/*
 * Program 137: Aggregation in C++
 *
 * This program demonstrates:
 * - Aggregation (Has-A relationship with weak ownership)
 * - Difference between composition and aggregation
 * - Independent lifetime of aggregated objects
 * - Pointers and references for aggregation
 * - Shared ownership patterns
 * - Lifetime management
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>

using namespace std;

// ===== COMPOSITION VS AGGREGATION =====

// Composition: Strong ownership - Engine dies with Car
class Engine {
private:
    string type;

public:
    Engine(const string& t) : type(t) {
        cout << "Engine created: " << type << endl;
    }

    ~Engine() {
        cout << "Engine destroyed: " << type << endl;
    }

    void start() {
        cout << type << " engine started" << endl;
    }
};

// This is COMPOSITION - Car owns Engine
class CarWithComposition {
private:
    string model;
    Engine engine;  // Engine is part of Car

public:
    CarWithComposition(const string& m, const string& engineType)
        : model(m), engine(engineType) {
        cout << "Car created (composition): " << model << endl;
    }

    ~CarWithComposition() {
        cout << "Car destroyed (composition): " << model << endl;
        // Engine automatically destroyed
    }
};

// ===== BASIC AGGREGATION =====

class Driver {
private:
    string name;
    int id;

public:
    Driver(const string& n, int i) : name(n), id(i) {
        cout << "Driver created: " << name << " (ID: " << id << ")" << endl;
    }

    ~Driver() {
        cout << "Driver destroyed: " << name << endl;
    }

    void drive() {
        cout << name << " is driving" << endl;
    }

    string getName() const { return name; }
    int getId() const { return id; }
};

// This is AGGREGATION - Car uses Driver but doesn't own it
class CarWithAggregation {
private:
    string model;
    Driver* driver;  // Pointer to Driver - weak ownership

public:
    CarWithAggregation(const string& m) : model(m), driver(nullptr) {
        cout << "Car created (aggregation): " << model << endl;
    }

    ~CarWithAggregation() {
        cout << "Car destroyed (aggregation): " << model << endl;
        // Driver NOT destroyed - it exists independently
    }

    void assignDriver(Driver* d) {
        driver = d;
        if (driver) {
            cout << "Driver " << driver->getName()
                 << " assigned to " << model << endl;
        }
    }

    void removeDriver() {
        if (driver) {
            cout << "Driver " << driver->getName()
                 << " removed from " << model << endl;
        }
        driver = nullptr;
    }

    void startDriving() {
        if (driver) {
            cout << model << " starting with driver " << driver->getName() << endl;
            driver->drive();
        } else {
            cout << model << " has no driver assigned" << endl;
        }
    }
};

// ===== UNIVERSITY AND PROFESSOR AGGREGATION =====

class Professor {
private:
    string name;
    string specialization;
    int employeeId;

public:
    Professor(const string& n, const string& spec, int id)
        : name(n), specialization(spec), employeeId(id) {
        cout << "Professor hired: " << name << " (" << specialization << ")" << endl;
    }

    ~Professor() {
        cout << "Professor retired: " << name << endl;
    }

    void teach(const string& course) {
        cout << "Prof. " << name << " teaching " << course << endl;
    }

    string getName() const { return name; }
    string getSpecialization() const { return specialization; }
};

class Department {
private:
    string name;
    vector<Professor*> professors;  // Aggregation - professors exist independently

public:
    Department(const string& n) : name(n) {
        cout << "Department created: " << name << endl;
    }

    ~Department() {
        cout << "Department closed: " << name << endl;
        // Professors are NOT deleted - they may work in other departments
    }

    void addProfessor(Professor* prof) {
        professors.push_back(prof);
        cout << "Prof. " << prof->getName() << " joined " << name << endl;
    }

    void removeProfessor(Professor* prof) {
        auto it = find(professors.begin(), professors.end(), prof);
        if (it != professors.end()) {
            cout << "Prof. " << (*it)->getName() << " left " << name << endl;
            professors.erase(it);
        }
    }

    void listProfessors() const {
        cout << "\nProfessors in " << name << " Department:" << endl;
        for (const auto& prof : professors) {
            cout << "  - " << prof->getName()
                 << " (" << prof->getSpecialization() << ")" << endl;
        }
    }

    void conductClass(const string& course) {
        if (!professors.empty()) {
            professors[0]->teach(course);
        } else {
            cout << "No professors available in " << name << endl;
        }
    }
};

// ===== TEAM AND PLAYER AGGREGATION =====

class Player {
private:
    string name;
    int jerseyNumber;
    string position;

public:
    Player(const string& n, int num, const string& pos)
        : name(n), jerseyNumber(num), position(pos) {
        cout << "Player created: #" << jerseyNumber << " " << name
             << " (" << position << ")" << endl;
    }

    ~Player() {
        cout << "Player retired: " << name << endl;
    }

    void play() {
        cout << name << " (#" << jerseyNumber << ") is playing " << position << endl;
    }

    string getName() const { return name; }
    int getJerseyNumber() const { return jerseyNumber; }
};

class Team {
private:
    string teamName;
    vector<Player*> roster;  // Aggregation - players can be traded

public:
    Team(const string& name) : teamName(name) {
        cout << "Team formed: " << teamName << endl;
    }

    ~Team() {
        cout << "Team disbanded: " << teamName << endl;
        // Players NOT deleted - they continue to exist
    }

    void addPlayer(Player* player) {
        roster.push_back(player);
        cout << player->getName() << " joined " << teamName << endl;
    }

    void removePlayer(Player* player) {
        auto it = find(roster.begin(), roster.end(), player);
        if (it != roster.end()) {
            cout << (*it)->getName() << " left " << teamName << endl;
            roster.erase(it);
        }
    }

    void displayRoster() const {
        cout << "\n" << teamName << " Roster:" << endl;
        for (const auto& player : roster) {
            cout << "  #" << player->getJerseyNumber() << " "
                 << player->getName() << endl;
        }
    }

    void playGame() {
        cout << "\n" << teamName << " is playing:" << endl;
        for (auto& player : roster) {
            player->play();
        }
    }
};

// ===== LIBRARY AND BOOK (SHARED) =====

class Book {
private:
    string title;
    string author;

public:
    Book(const string& t, const string& a) : title(t), author(a) {
        cout << "Book published: \"" << title << "\" by " << author << endl;
    }

    ~Book() {
        cout << "Book out of print: \"" << title << "\"" << endl;
    }

    void display() const {
        cout << "  \"" << title << "\" by " << author << endl;
    }

    string getTitle() const { return title; }
};

class LibraryAggregation {
private:
    string libraryName;
    vector<shared_ptr<Book>> books;  // Shared ownership

public:
    LibraryAggregation(const string& name) : libraryName(name) {
        cout << "Library opened: " << libraryName << endl;
    }

    ~LibraryAggregation() {
        cout << "Library closed: " << libraryName << endl;
    }

    void addBook(shared_ptr<Book> book) {
        books.push_back(book);
        cout << "Book added to " << libraryName << endl;
    }

    void removeBook(shared_ptr<Book> book) {
        auto it = find(books.begin(), books.end(), book);
        if (it != books.end()) {
            books.erase(it);
            cout << "Book removed from " << libraryName << endl;
        }
    }

    void displayCatalog() const {
        cout << "\n" << libraryName << " Catalog:" << endl;
        for (const auto& book : books) {
            book->display();
        }
    }
};

// ===== STUDENT AND COURSE AGGREGATION (MANY-TO-MANY) =====

class Course;

class Student {
private:
    string name;
    int studentId;
    vector<Course*> enrolledCourses;  // Aggregation

public:
    Student(const string& n, int id) : name(n), studentId(id) {
        cout << "Student enrolled: " << name << " (ID: " << id << ")" << endl;
    }

    ~Student() {
        cout << "Student graduated: " << name << endl;
    }

    void enrollInCourse(Course* course);

    void dropCourse(Course* course) {
        auto it = find(enrolledCourses.begin(), enrolledCourses.end(), course);
        if (it != enrolledCourses.end()) {
            enrolledCourses.erase(it);
            cout << name << " dropped a course" << endl;
        }
    }

    void listCourses() const;

    string getName() const { return name; }
    int getId() const { return studentId; }
};

class Course {
private:
    string courseName;
    string courseCode;
    vector<Student*> enrolledStudents;  // Aggregation

public:
    Course(const string& name, const string& code)
        : courseName(name), courseCode(code) {
        cout << "Course created: " << courseCode << " - " << courseName << endl;
    }

    ~Course() {
        cout << "Course ended: " << courseCode << endl;
    }

    void addStudent(Student* student) {
        enrolledStudents.push_back(student);
        cout << student->getName() << " enrolled in " << courseCode << endl;
    }

    void removeStudent(Student* student) {
        auto it = find(enrolledStudents.begin(), enrolledStudents.end(), student);
        if (it != enrolledStudents.end()) {
            enrolledStudents.erase(it);
        }
    }

    void listStudents() const {
        cout << "\nStudents in " << courseCode << ":" << endl;
        for (const auto& student : enrolledStudents) {
            cout << "  - " << student->getName()
                 << " (ID: " << student->getId() << ")" << endl;
        }
    }

    string getName() const { return courseName; }
    string getCode() const { return courseCode; }
};

void Student::enrollInCourse(Course* course) {
    enrolledCourses.push_back(course);
    course->addStudent(this);
}

void Student::listCourses() const {
    cout << "\nCourses for " << name << ":" << endl;
    for (const auto& course : enrolledCourses) {
        cout << "  - " << course->getCode() << ": " << course->getName() << endl;
    }
}

int main() {
    cout << "=== Program 137: Aggregation ===" << endl;
    cout << "================================\n" << endl;

    // 1. Composition vs Aggregation
    cout << "1. Composition vs Aggregation Comparison" << endl;
    cout << "-----------------------------------------" << endl;
    {
        cout << "\nComposition example:" << endl;
        CarWithComposition compositionCar("Honda Civic", "Inline-4");
        // Engine is destroyed with car

        cout << "\nAggregation example:" << endl;
        Driver driver1("John Smith", 1001);
        CarWithAggregation aggregationCar("Toyota Camry");
        aggregationCar.assignDriver(&driver1);
        aggregationCar.startDriving();
        // Driver survives after car is destroyed

        cout << "\nDestroying objects:" << endl;
    }
    cout << "Driver still exists after car is destroyed!\n" << endl;

    // 2. Department and Professors
    cout << "\n2. University Departments and Professors" << endl;
    cout << "------------------------------------------" << endl;
    {
        Professor prof1("Dr. Smith", "Computer Science", 101);
        Professor prof2("Dr. Johnson", "Mathematics", 102);
        Professor prof3("Dr. Williams", "Computer Science", 103);

        cout << "\nCreating departments:" << endl;
        Department csDept("Computer Science");
        Department mathDept("Mathematics");

        csDept.addProfessor(&prof1);
        csDept.addProfessor(&prof3);
        mathDept.addProfessor(&prof2);

        // Prof can work in multiple departments
        mathDept.addProfessor(&prof1);

        csDept.listProfessors();
        mathDept.listProfessors();

        cout << "\nConducting classes:" << endl;
        csDept.conductClass("Data Structures");
        mathDept.conductClass("Linear Algebra");

        cout << "\nDepartments closing (professors remain):" << endl;
    }

    // 3. Team and Players
    cout << "\n\n3. Sports Team and Players" << endl;
    cout << "----------------------------" << endl;
    {
        Player player1("Michael Jordan", 23, "Shooting Guard");
        Player player2("LeBron James", 23, "Small Forward");
        Player player3("Stephen Curry", 30, "Point Guard");

        Team bulls("Chicago Bulls");
        Team warriors("Golden State Warriors");

        bulls.addPlayer(&player1);
        warriors.addPlayer(&player2);
        warriors.addPlayer(&player3);

        bulls.displayRoster();
        warriors.displayRoster();

        cout << "\nPlayer trade:" << endl;
        bulls.removePlayer(&player1);
        warriors.addPlayer(&player1);

        warriors.displayRoster();
        warriors.playGame();

        cout << "\nTeams disbanded (players continue to exist):" << endl;
    }

    // 4. Library with shared books
    cout << "\n\n4. Multiple Libraries Sharing Books" << endl;
    cout << "------------------------------------" << endl;
    {
        auto book1 = make_shared<Book>("1984", "George Orwell");
        auto book2 = make_shared<Book>("To Kill a Mockingbird", "Harper Lee");
        auto book3 = make_shared<Book>("The Great Gatsby", "F. Scott Fitzgerald");

        LibraryAggregation library1("City Library");
        LibraryAggregation library2("University Library");

        library1.addBook(book1);
        library1.addBook(book2);
        library2.addBook(book2);  // Same book in multiple libraries
        library2.addBook(book3);

        library1.displayCatalog();
        library2.displayCatalog();

        cout << "\nRemoving book from one library:" << endl;
        library1.removeBook(book2);

        library1.displayCatalog();
        library2.displayCatalog();  // Still has the book

        cout << "\nLibraries closing:" << endl;
    }
    cout << "Books exist independently" << endl;

    // 5. Many-to-many relationship: Students and Courses
    cout << "\n\n5. Many-to-Many: Students and Courses" << endl;
    cout << "---------------------------------------" << endl;
    {
        Student alice("Alice Johnson", 2001);
        Student bob("Bob Smith", 2002);
        Student charlie("Charlie Brown", 2003);

        Course cpp("C++ Programming", "CS201");
        Course dataStructures("Data Structures", "CS202");
        Course algorithms("Algorithms", "CS301");

        cout << "\nStudent enrollment:" << endl;
        alice.enrollInCourse(&cpp);
        alice.enrollInCourse(&dataStructures);
        bob.enrollInCourse(&cpp);
        bob.enrollInCourse(&algorithms);
        charlie.enrollInCourse(&dataStructures);
        charlie.enrollInCourse(&algorithms);

        cpp.listStudents();
        dataStructures.listStudents();

        alice.listCourses();
        bob.listCourses();

        cout << "\nCourses and students can exist independently" << endl;
    }

    // 6. Driver switching cars
    cout << "\n\n6. Driver Switching Between Cars" << endl;
    cout << "----------------------------------" << endl;
    {
        Driver driver("Sarah Connor", 3001);

        CarWithAggregation car1("Tesla Model 3");
        CarWithAggregation car2("BMW i8");

        cout << "\nDriver using car1:" << endl;
        car1.assignDriver(&driver);
        car1.startDriving();

        cout << "\nDriver switching to car2:" << endl;
        car1.removeDriver();
        car2.assignDriver(&driver);
        car2.startDriving();

        cout << "\nCars destroyed (driver remains):" << endl;
    }

    cout << "\n\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Aggregation - 'has-a' with weak ownership" << endl;
    cout << "2. Independent lifetime - aggregated objects survive container" << endl;
    cout << "3. Composition vs Aggregation - strong vs weak ownership" << endl;
    cout << "4. Pointers/references for aggregation" << endl;
    cout << "5. Many-to-many relationships" << endl;
    cout << "6. Shared ownership with shared_ptr" << endl;
    cout << "7. Objects can belong to multiple containers" << endl;
    cout << "8. Container doesn't destroy aggregated objects" << endl;
    cout << "9. Flexible object relationships" << endl;
    cout << "10. Real-world modeling - students/courses, teams/players" << endl;

    return 0;
}
