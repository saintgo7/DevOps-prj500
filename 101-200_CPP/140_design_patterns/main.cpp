/*
 * Program 140: Design Patterns in C++
 *
 * This program demonstrates:
 * - Singleton Pattern - single instance
 * - Factory Pattern - object creation
 * - Abstract Factory Pattern
 * - Observer Pattern - event notification
 * - Strategy Pattern - algorithm selection
 * - Decorator Pattern - adding functionality
 * - Builder Pattern - complex object construction
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>

using namespace std;

// ===== SINGLETON PATTERN =====

class Logger {
private:
    static Logger* instance;
    vector<string> logs;

    // Private constructor prevents external instantiation
    Logger() {
        cout << "Logger instance created" << endl;
    }

    // Prevent copying
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

public:
    static Logger* getInstance() {
        if (instance == nullptr) {
            instance = new Logger();
        }
        return instance;
    }

    void log(const string& message) {
        logs.push_back(message);
        cout << "[LOG] " << message << endl;
    }

    void displayLogs() const {
        cout << "\n=== All Logs ===" << endl;
        for (size_t i = 0; i < logs.size(); i++) {
            cout << i + 1 << ". " << logs[i] << endl;
        }
    }

    static void destroy() {
        delete instance;
        instance = nullptr;
    }
};

Logger* Logger::instance = nullptr;

// ===== FACTORY PATTERN =====

// Product interface
class Shape {
public:
    virtual ~Shape() {}
    virtual void draw() const = 0;
    virtual double area() const = 0;
};

// Concrete products
class Circle : public Shape {
private:
    double radius;

public:
    Circle(double r) : radius(r) {}

    void draw() const override {
        cout << "Drawing Circle with radius " << radius << endl;
    }

    double area() const override {
        return 3.14159 * radius * radius;
    }
};

class Rectangle : public Shape {
private:
    double width, height;

public:
    Rectangle(double w, double h) : width(w), height(h) {}

    void draw() const override {
        cout << "Drawing Rectangle " << width << "x" << height << endl;
    }

    double area() const override {
        return width * height;
    }
};

class Triangle : public Shape {
private:
    double base, height;

public:
    Triangle(double b, double h) : base(b), height(h) {}

    void draw() const override {
        cout << "Drawing Triangle with base " << base << " and height " << height << endl;
    }

    double area() const override {
        return 0.5 * base * height;
    }
};

// Factory
class ShapeFactory {
public:
    enum ShapeType { CIRCLE, RECTANGLE, TRIANGLE };

    static unique_ptr<Shape> createShape(ShapeType type, double param1, double param2 = 0) {
        switch (type) {
            case CIRCLE:
                return make_unique<Circle>(param1);
            case RECTANGLE:
                return make_unique<Rectangle>(param1, param2);
            case TRIANGLE:
                return make_unique<Triangle>(param1, param2);
            default:
                return nullptr;
        }
    }
};

// ===== ABSTRACT FACTORY PATTERN =====

// Abstract products
class Button {
public:
    virtual ~Button() {}
    virtual void render() const = 0;
};

class Checkbox {
public:
    virtual ~Checkbox() {}
    virtual void render() const = 0;
};

// Concrete products - Windows
class WindowsButton : public Button {
public:
    void render() const override {
        cout << "Rendering Windows-style button" << endl;
    }
};

class WindowsCheckbox : public Checkbox {
public:
    void render() const override {
        cout << "Rendering Windows-style checkbox" << endl;
    }
};

// Concrete products - Mac
class MacButton : public Button {
public:
    void render() const override {
        cout << "Rendering Mac-style button" << endl;
    }
};

class MacCheckbox : public Checkbox {
public:
    void render() const override {
        cout << "Rendering Mac-style checkbox" << endl;
    }
};

// Abstract factory
class GUIFactory {
public:
    virtual ~GUIFactory() {}
    virtual unique_ptr<Button> createButton() const = 0;
    virtual unique_ptr<Checkbox> createCheckbox() const = 0;
};

// Concrete factories
class WindowsFactory : public GUIFactory {
public:
    unique_ptr<Button> createButton() const override {
        return make_unique<WindowsButton>();
    }

    unique_ptr<Checkbox> createCheckbox() const override {
        return make_unique<WindowsCheckbox>();
    }
};

class MacFactory : public GUIFactory {
public:
    unique_ptr<Button> createButton() const override {
        return make_unique<MacButton>();
    }

    unique_ptr<Checkbox> createCheckbox() const override {
        return make_unique<MacCheckbox>();
    }
};

// ===== OBSERVER PATTERN =====

class Observer {
public:
    virtual ~Observer() {}
    virtual void update(const string& message) = 0;
};

class Subject {
private:
    vector<Observer*> observers;
    string state;

public:
    void attach(Observer* observer) {
        observers.push_back(observer);
        cout << "Observer attached" << endl;
    }

    void detach(Observer* observer) {
        auto it = find(observers.begin(), observers.end(), observer);
        if (it != observers.end()) {
            observers.erase(it);
            cout << "Observer detached" << endl;
        }
    }

    void setState(const string& newState) {
        state = newState;
        notify();
    }

    string getState() const {
        return state;
    }

private:
    void notify() {
        cout << "\nNotifying " << observers.size() << " observers..." << endl;
        for (auto observer : observers) {
            observer->update(state);
        }
    }
};

class EmailNotifier : public Observer {
private:
    string email;

public:
    EmailNotifier(const string& e) : email(e) {}

    void update(const string& message) override {
        cout << "Email to " << email << ": " << message << endl;
    }
};

class SMSNotifier : public Observer {
private:
    string phone;

public:
    SMSNotifier(const string& p) : phone(p) {}

    void update(const string& message) override {
        cout << "SMS to " << phone << ": " << message << endl;
    }
};

// ===== STRATEGY PATTERN =====

// Strategy interface
class SortStrategy {
public:
    virtual ~SortStrategy() {}
    virtual void sort(vector<int>& data) const = 0;
    virtual string getName() const = 0;
};

// Concrete strategies
class BubbleSort : public SortStrategy {
public:
    void sort(vector<int>& data) const override {
        cout << "Sorting using Bubble Sort" << endl;
        // Simplified bubble sort
        for (size_t i = 0; i < data.size(); i++) {
            for (size_t j = 0; j < data.size() - 1; j++) {
                if (data[j] > data[j + 1]) {
                    swap(data[j], data[j + 1]);
                }
            }
        }
    }

    string getName() const override { return "Bubble Sort"; }
};

class QuickSort : public SortStrategy {
public:
    void sort(vector<int>& data) const override {
        cout << "Sorting using Quick Sort" << endl;
        std::sort(data.begin(), data.end());
    }

    string getName() const override { return "Quick Sort"; }
};

// Context
class Sorter {
private:
    unique_ptr<SortStrategy> strategy;

public:
    void setStrategy(unique_ptr<SortStrategy> s) {
        strategy = std::move(s);
    }

    void sortData(vector<int>& data) const {
        if (strategy) {
            cout << "Using " << strategy->getName() << endl;
            strategy->sort(data);
        }
    }
};

// ===== DECORATOR PATTERN =====

// Component interface
class Coffee {
public:
    virtual ~Coffee() {}
    virtual string getDescription() const = 0;
    virtual double cost() const = 0;
};

// Concrete component
class SimpleCoffee : public Coffee {
public:
    string getDescription() const override {
        return "Simple Coffee";
    }

    double cost() const override {
        return 2.0;
    }
};

// Decorator base
class CoffeeDecorator : public Coffee {
protected:
    unique_ptr<Coffee> coffee;

public:
    CoffeeDecorator(unique_ptr<Coffee> c) : coffee(std::move(c)) {}
};

// Concrete decorators
class Milk : public CoffeeDecorator {
public:
    Milk(unique_ptr<Coffee> c) : CoffeeDecorator(std::move(c)) {}

    string getDescription() const override {
        return coffee->getDescription() + ", Milk";
    }

    double cost() const override {
        return coffee->cost() + 0.5;
    }
};

class Sugar : public CoffeeDecorator {
public:
    Sugar(unique_ptr<Coffee> c) : CoffeeDecorator(std::move(c)) {}

    string getDescription() const override {
        return coffee->getDescription() + ", Sugar";
    }

    double cost() const override {
        return coffee->cost() + 0.2;
    }
};

class WhippedCream : public CoffeeDecorator {
public:
    WhippedCream(unique_ptr<Coffee> c) : CoffeeDecorator(std::move(c)) {}

    string getDescription() const override {
        return coffee->getDescription() + ", Whipped Cream";
    }

    double cost() const override {
        return coffee->cost() + 0.7;
    }
};

// ===== BUILDER PATTERN =====

class Computer {
private:
    string cpu;
    string gpu;
    int ram;
    int storage;
    string os;

public:
    void setCPU(const string& c) { cpu = c; }
    void setGPU(const string& g) { gpu = g; }
    void setRAM(int r) { ram = r; }
    void setStorage(int s) { storage = s; }
    void setOS(const string& o) { os = o; }

    void display() const {
        cout << "\n=== Computer Configuration ===" << endl;
        cout << "CPU: " << cpu << endl;
        cout << "GPU: " << gpu << endl;
        cout << "RAM: " << ram << " GB" << endl;
        cout << "Storage: " << storage << " GB" << endl;
        cout << "OS: " << os << endl;
    }
};

class ComputerBuilder {
private:
    unique_ptr<Computer> computer;

public:
    ComputerBuilder() {
        computer = make_unique<Computer>();
    }

    ComputerBuilder& setCPU(const string& cpu) {
        computer->setCPU(cpu);
        return *this;
    }

    ComputerBuilder& setGPU(const string& gpu) {
        computer->setGPU(gpu);
        return *this;
    }

    ComputerBuilder& setRAM(int ram) {
        computer->setRAM(ram);
        return *this;
    }

    ComputerBuilder& setStorage(int storage) {
        computer->setStorage(storage);
        return *this;
    }

    ComputerBuilder& setOS(const string& os) {
        computer->setOS(os);
        return *this;
    }

    unique_ptr<Computer> build() {
        return std::move(computer);
    }
};

int main() {
    cout << "=== Program 140: Design Patterns ===" << endl;
    cout << "====================================\n" << endl;

    // 1. Singleton Pattern
    cout << "1. Singleton Pattern - Logger" << endl;
    cout << "------------------------------" << endl;
    {
        Logger* logger1 = Logger::getInstance();
        logger1->log("Application started");
        logger1->log("User logged in");

        Logger* logger2 = Logger::getInstance();
        logger2->log("Data loaded");

        cout << "logger1 == logger2: " << (logger1 == logger2 ? "Yes" : "No") << endl;

        logger1->displayLogs();
        Logger::destroy();
    }

    // 2. Factory Pattern
    cout << "\n\n2. Factory Pattern - Shape Creation" << endl;
    cout << "------------------------------------" << endl;
    {
        auto circle = ShapeFactory::createShape(ShapeFactory::CIRCLE, 5.0);
        auto rectangle = ShapeFactory::createShape(ShapeFactory::RECTANGLE, 4.0, 6.0);
        auto triangle = ShapeFactory::createShape(ShapeFactory::TRIANGLE, 3.0, 4.0);

        circle->draw();
        cout << "Area: " << circle->area() << endl;

        rectangle->draw();
        cout << "Area: " << rectangle->area() << endl;

        triangle->draw();
        cout << "Area: " << triangle->area() << endl;
    }

    // 3. Abstract Factory Pattern
    cout << "\n\n3. Abstract Factory Pattern - GUI Components" << endl;
    cout << "---------------------------------------------" << endl;
    {
        cout << "Windows theme:" << endl;
        unique_ptr<GUIFactory> windowsFactory = make_unique<WindowsFactory>();
        auto winButton = windowsFactory->createButton();
        auto winCheckbox = windowsFactory->createCheckbox();
        winButton->render();
        winCheckbox->render();

        cout << "\nMac theme:" << endl;
        unique_ptr<GUIFactory> macFactory = make_unique<MacFactory>();
        auto macButton = macFactory->createButton();
        auto macCheckbox = macFactory->createCheckbox();
        macButton->render();
        macCheckbox->render();
    }

    // 4. Observer Pattern
    cout << "\n\n4. Observer Pattern - Notification System" << endl;
    cout << "------------------------------------------" << endl;
    {
        Subject weatherStation;

        EmailNotifier email1("user1@example.com");
        EmailNotifier email2("user2@example.com");
        SMSNotifier sms1("555-1234");

        weatherStation.attach(&email1);
        weatherStation.attach(&email2);
        weatherStation.attach(&sms1);

        weatherStation.setState("Temperature: 72°F, Sunny");

        cout << "\nRemoving one observer:" << endl;
        weatherStation.detach(&email2);

        weatherStation.setState("Temperature: 68°F, Cloudy");
    }

    // 5. Strategy Pattern
    cout << "\n\n5. Strategy Pattern - Sorting Algorithms" << endl;
    cout << "-----------------------------------------" << endl;
    {
        vector<int> data1 = {5, 2, 8, 1, 9};
        vector<int> data2 = {5, 2, 8, 1, 9};

        Sorter sorter;

        cout << "Original: ";
        for (int n : data1) cout << n << " ";
        cout << endl;

        sorter.setStrategy(make_unique<BubbleSort>());
        sorter.sortData(data1);
        cout << "Sorted: ";
        for (int n : data1) cout << n << " ";
        cout << endl;

        cout << "\nOriginal: ";
        for (int n : data2) cout << n << " ";
        cout << endl;

        sorter.setStrategy(make_unique<QuickSort>());
        sorter.sortData(data2);
        cout << "Sorted: ";
        for (int n : data2) cout << n << " ";
        cout << endl;
    }

    // 6. Decorator Pattern
    cout << "\n\n6. Decorator Pattern - Coffee Shop" << endl;
    cout << "-----------------------------------" << endl;
    {
        unique_ptr<Coffee> coffee = make_unique<SimpleCoffee>();
        cout << coffee->getDescription() << " - $" << coffee->cost() << endl;

        coffee = make_unique<Milk>(std::move(coffee));
        cout << coffee->getDescription() << " - $" << coffee->cost() << endl;

        coffee = make_unique<Sugar>(std::move(coffee));
        cout << coffee->getDescription() << " - $" << coffee->cost() << endl;

        coffee = make_unique<WhippedCream>(std::move(coffee));
        cout << coffee->getDescription() << " - $" << coffee->cost() << endl;
    }

    // 7. Builder Pattern
    cout << "\n\n7. Builder Pattern - Computer Configuration" << endl;
    cout << "--------------------------------------------" << endl;
    {
        auto gamingPC = ComputerBuilder()
            .setCPU("Intel i9-13900K")
            .setGPU("NVIDIA RTX 4090")
            .setRAM(64)
            .setStorage(2000)
            .setOS("Windows 11")
            .build();

        gamingPC->display();

        auto workstation = ComputerBuilder()
            .setCPU("AMD Ryzen 9 7950X")
            .setGPU("NVIDIA RTX 4080")
            .setRAM(128)
            .setStorage(4000)
            .setOS("Ubuntu 22.04")
            .build();

        workstation->display();
    }

    // 8. Combining patterns
    cout << "\n\n8. Combining Patterns" << endl;
    cout << "----------------------" << endl;
    {
        Logger* logger = Logger::getInstance();
        logger->log("Creating shapes using Factory pattern");

        auto shape1 = ShapeFactory::createShape(ShapeFactory::CIRCLE, 10.0);
        auto shape2 = ShapeFactory::createShape(ShapeFactory::RECTANGLE, 5.0, 8.0);

        logger->log("Shapes created successfully");

        shape1->draw();
        shape2->draw();

        Logger::destroy();
    }

    cout << "\n\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Singleton - single instance, global access" << endl;
    cout << "2. Factory - encapsulate object creation" << endl;
    cout << "3. Abstract Factory - families of related objects" << endl;
    cout << "4. Observer - one-to-many dependency, event notification" << endl;
    cout << "5. Strategy - interchangeable algorithms" << endl;
    cout << "6. Decorator - add responsibilities dynamically" << endl;
    cout << "7. Builder - construct complex objects step-by-step" << endl;
    cout << "8. Design patterns solve common OOP problems" << endl;
    cout << "9. Patterns can be combined for more complex solutions" << endl;
    cout << "10. Each pattern has specific use cases and trade-offs" << endl;

    cout << "\nDesign Pattern Categories:" << endl;
    cout << "- Creational: Singleton, Factory, Abstract Factory, Builder" << endl;
    cout << "- Structural: Decorator, Adapter, Composite, Facade" << endl;
    cout << "- Behavioral: Observer, Strategy, Command, State" << endl;

    return 0;
}
