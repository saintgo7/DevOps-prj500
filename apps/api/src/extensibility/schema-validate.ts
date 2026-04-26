// Minimal JSON Schema validator for CustomDomain payloads (ADR-0020 §B).
//
// We deliberately avoid pulling in a full Ajv/Zod dependency for MVP —
// the surface we need is small and well-defined. We support:
//   type: 'object' | 'array' | 'string' | 'number' | 'integer' | 'boolean' | 'null'
//   required: string[]                       (object)
//   properties: Record<string, schema>       (object)
//   additionalProperties: boolean | schema   (object; defaults to true)
//   items: schema                            (array)
//   minLength / maxLength                    (string)
//   minimum / maximum                        (number / integer)
//   enum: unknown[]                          (any)
//   pattern: string (RegExp)                 (string)
//
// Anything else is ignored (forward-compatible). For richer validation we
// add a real schema lib in a follow-up ADR and replace this module.

export interface JsonSchema {
  type?: string;
  required?: string[];
  properties?: Record<string, JsonSchema>;
  additionalProperties?: boolean | JsonSchema;
  items?: JsonSchema;
  minLength?: number;
  maxLength?: number;
  minimum?: number;
  maximum?: number;
  enum?: unknown[];
  pattern?: string;
}

export interface ValidationError {
  path: string;
  message: string;
}

export interface ValidationResult {
  ok: boolean;
  errors: ValidationError[];
}

function typeOf(value: unknown): string {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  if (Number.isInteger(value)) return 'integer';
  return typeof value;
}

function checkType(value: unknown, type: string): boolean {
  const actual = typeOf(value);
  if (type === 'number') return actual === 'number' || actual === 'integer';
  return actual === type;
}

function appendPath(path: string, segment: string | number): string {
  if (typeof segment === 'number') return `${path}[${segment}]`;
  return path === '' ? segment : `${path}.${segment}`;
}

export function validatePayload(value: unknown, schema: JsonSchema): ValidationResult {
  const errors: ValidationError[] = [];
  walk(value, schema, '', errors);
  return { ok: errors.length === 0, errors };
}

function walk(value: unknown, schema: JsonSchema, path: string, errors: ValidationError[]): void {
  if (schema.type && !checkType(value, schema.type)) {
    errors.push({
      path: path || '<root>',
      message: `expected type '${schema.type}', got '${typeOf(value)}'`,
    });
    return;
  }
  if (schema.enum && !schema.enum.some((v) => Object.is(v, value) || v === value)) {
    errors.push({
      path: path || '<root>',
      message: `value not in enum (${schema.enum.length} options)`,
    });
  }

  if (schema.type === 'string' && typeof value === 'string') {
    if (schema.minLength !== undefined && value.length < schema.minLength) {
      errors.push({ path: path || '<root>', message: `string too short (< ${schema.minLength})` });
    }
    if (schema.maxLength !== undefined && value.length > schema.maxLength) {
      errors.push({ path: path || '<root>', message: `string too long (> ${schema.maxLength})` });
    }
    if (schema.pattern) {
      try {
        const re = new RegExp(schema.pattern);
        if (!re.test(value)) {
          errors.push({ path: path || '<root>', message: `pattern mismatch /${schema.pattern}/` });
        }
      } catch {
        errors.push({ path: path || '<root>', message: `invalid pattern /${schema.pattern}/` });
      }
    }
  }

  if (
    (schema.type === 'number' || schema.type === 'integer') &&
    typeof value === 'number'
  ) {
    if (schema.minimum !== undefined && value < schema.minimum) {
      errors.push({ path: path || '<root>', message: `value < minimum (${schema.minimum})` });
    }
    if (schema.maximum !== undefined && value > schema.maximum) {
      errors.push({ path: path || '<root>', message: `value > maximum (${schema.maximum})` });
    }
  }

  if (schema.type === 'object' && typeof value === 'object' && value !== null && !Array.isArray(value)) {
    const obj = value as Record<string, unknown>;
    if (schema.required) {
      for (const key of schema.required) {
        if (!(key in obj)) {
          errors.push({ path: appendPath(path, key), message: 'required property missing' });
        }
      }
    }
    const props = schema.properties ?? {};
    for (const [key, child] of Object.entries(obj)) {
      const childSchema = props[key];
      if (childSchema) {
        walk(child, childSchema, appendPath(path, key), errors);
      } else {
        const ap = schema.additionalProperties;
        if (ap === false) {
          errors.push({ path: appendPath(path, key), message: 'additional property not allowed' });
        } else if (typeof ap === 'object' && ap !== null) {
          walk(child, ap, appendPath(path, key), errors);
        }
      }
    }
  }

  if (schema.type === 'array' && Array.isArray(value) && schema.items) {
    value.forEach((item, idx) => {
      walk(item, schema.items as JsonSchema, appendPath(path, idx), errors);
    });
  }
}
