import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import {
  NeedsService,
  type CreateOfferInput,
  type CreateRequestInput,
} from './needs.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const REQ = '33333333-3333-3333-3333-333333333333';
const OFF = '44444444-4444-4444-4444-444444444444';
const MATCH = '55555555-5555-5555-5555-555555555555';
const VERIFIER = '66666666-6666-6666-6666-666666666666';

function reqInput(overrides: Partial<CreateRequestInput> = {}): CreateRequestInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    category: 'relief',
    primaryLocale: 'ko',
    bodyI18n: { ko: { title: '구호 물품 요청', description: '벵골만 침수 지역에 정수 도구가 필요합니다.' } },
    sdgFocus: ['SDG-6'],
    region: 'BD',
    quantity: 100,
    unit: 'units',
    urgency: 'critical',
    neededBy: new Date(Date.now() + 7 * 86400_000),
    ...overrides,
  };
}

function offInput(overrides: Partial<CreateOfferInput> = {}): CreateOfferInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    category: 'relief',
    primaryLocale: 'ko',
    bodyI18n: { ko: { title: '정수 도구 제공', description: '서울에서 100개 단위로 보낼 수 있습니다.' } },
    sdgFocus: ['SDG-6'],
    region: 'KR',
    quantity: 100,
    unit: 'units',
    availableUntil: new Date(Date.now() + 14 * 86400_000),
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const req = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: REQ, ...(data as object) })),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const off = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: OFF, ...(data as object) })),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const match = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: MATCH, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const ful = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  return {
    needRequest: req,
    offerListing: off,
    needMatch: match,
    needFulfillment: ful,
  } as unknown as PrismaService;
}

describe('NeedsService.createRequest', () => {
  it('rejects quantity 0', async () => {
    const svc = new NeedsService(prismaStub());
    await expect(svc.createRequest(reqInput({ quantity: 0 }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('rejects past neededBy', async () => {
    const svc = new NeedsService(prismaStub());
    await expect(
      svc.createRequest(reqInput({ neededBy: new Date(Date.now() - 86400_000) })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('creates a draft request', async () => {
    const prisma = prismaStub();
    const svc = new NeedsService(prisma);
    await svc.createRequest(reqInput());
    expect(prisma.needRequest.create).toHaveBeenCalledOnce();
  });
});

describe('NeedsService.createOffer', () => {
  it('rejects past availableUntil', async () => {
    const svc = new NeedsService(prismaStub());
    await expect(
      svc.createOffer(offInput({ availableUntil: new Date(Date.now() - 86400_000) })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('creates a draft offer', async () => {
    const prisma = prismaStub();
    const svc = new NeedsService(prisma);
    await svc.createOffer(offInput());
    expect(prisma.offerListing.create).toHaveBeenCalledOnce();
  });
});

describe('NeedsService.suggestMatch', () => {
  it('rejects mismatched categories', async () => {
    const prisma = prismaStub();
    (prisma.needRequest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: REQ,
      category: 'relief',
      state: 'published',
    });
    (prisma.offerListing.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: OFF,
      category: 'knowledge',
      state: 'published',
    });
    const svc = new NeedsService(prisma);
    await expect(svc.suggestMatch(TENANT, REQ, OFF)).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects when one side is in draft', async () => {
    const prisma = prismaStub();
    (prisma.needRequest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: REQ,
      category: 'relief',
      state: 'draft',
    });
    (prisma.offerListing.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: OFF,
      category: 'relief',
      state: 'published',
    });
    const svc = new NeedsService(prisma);
    await expect(svc.suggestMatch(TENANT, REQ, OFF)).rejects.toBeInstanceOf(ConflictException);
  });

  it('creates a suggested match', async () => {
    const prisma = prismaStub();
    (prisma.needRequest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: REQ,
      category: 'relief',
      state: 'published',
    });
    (prisma.offerListing.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: OFF,
      category: 'relief',
      state: 'published',
    });
    const svc = new NeedsService(prisma);
    await svc.suggestMatch(TENANT, REQ, OFF);
    expect(prisma.needMatch.create).toHaveBeenCalledOnce();
  });
});

describe('NeedsService.accept', () => {
  it('marks contacted on first acceptance, accepted on second', async () => {
    const prisma = prismaStub();
    // First acceptance (provider) — moves to contacted.
    (prisma.needMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      id: MATCH,
      state: 'suggested',
      requesterAcceptedAt: null,
      providerAcceptedAt: null,
    });
    (prisma.needMatch.update as ReturnType<typeof vi.fn>).mockResolvedValue({ id: MATCH });
    const svc = new NeedsService(prisma);
    await svc.accept(TENANT, MATCH, 'provider');
    const firstCall = (prisma.needMatch.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string; providerAcceptedAt?: Date };
    };
    expect(firstCall.data.state).toBe('contacted');
    expect(firstCall.data.providerAcceptedAt).toBeInstanceOf(Date);

    // Second acceptance (requester) — moves to accepted.
    (prisma.needMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      id: MATCH,
      state: 'contacted',
      requesterAcceptedAt: null,
      providerAcceptedAt: new Date(),
    });
    await svc.accept(TENANT, MATCH, 'requester');
    const secondCall = (prisma.needMatch.update as ReturnType<typeof vi.fn>).mock.calls[1]?.[0] as {
      data: { state: string };
    };
    expect(secondCall.data.state).toBe('accepted');
  });

  it('rejects double acceptance from the same side', async () => {
    const prisma = prismaStub();
    (prisma.needMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'contacted',
      requesterAcceptedAt: new Date(),
      providerAcceptedAt: null,
    });
    const svc = new NeedsService(prisma);
    await expect(svc.accept(TENANT, MATCH, 'requester')).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects acceptance after the match was cancelled', async () => {
    const prisma = prismaStub();
    (prisma.needMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'cancelled',
    });
    const svc = new NeedsService(prisma);
    await expect(svc.accept(TENANT, MATCH, 'requester')).rejects.toBeInstanceOf(ConflictException);
  });
});

describe('NeedsService.sign', () => {
  const fullClause =
    'I confirm receipt of the goods listed above and agree to the platform terms.';

  it('rejects sign before match is shipped', async () => {
    const prisma = prismaStub();
    (prisma.needMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'accepted',
    });
    const svc = new NeedsService(prisma);
    await expect(
      svc.sign(TENANT, MATCH, 'requester', fullClause),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('creates a fulfilment on first signature', async () => {
    const prisma = prismaStub();
    (prisma.needMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'shipped',
    });
    (prisma.needFulfillment.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new NeedsService(prisma);
    await svc.sign(TENANT, MATCH, 'provider', fullClause, 'TRACK-1', ['hash1', 'hash2']);
    expect(prisma.needFulfillment.create).toHaveBeenCalledOnce();
  });

  it('rejects mismatched clause hashes between signers', async () => {
    const prisma = prismaStub();
    (prisma.needMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'shipped',
    });
    (prisma.needFulfillment.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: 'fulfil-1',
      agreedClauseHash: 'different-hash',
      requesterSignedAt: null,
      providerSignedAt: new Date(),
    });
    const svc = new NeedsService(prisma);
    await expect(
      svc.sign(TENANT, MATCH, 'requester', fullClause),
    ).rejects.toBeInstanceOf(ConflictException);
  });
});

describe('NeedsService.setRequestVerification', () => {
  it('rejects unknown levels', async () => {
    const prisma = prismaStub();
    (prisma.needRequest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({ id: REQ });
    const svc = new NeedsService(prisma);
    await expect(
      // @ts-expect-error testing runtime guard
      svc.setRequestVerification(TENANT, REQ, 'super-trusted', VERIFIER),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('records a verification', async () => {
    const prisma = prismaStub();
    (prisma.needRequest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({ id: REQ });
    const svc = new NeedsService(prisma);
    await svc.setRequestVerification(TENANT, REQ, 'verified', VERIFIER);
    expect(prisma.needRequest.update).toHaveBeenCalledOnce();
  });
});
