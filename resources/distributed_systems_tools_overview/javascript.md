# JavaScript

## How does JavaScript work?

JavaScript runs on a JavaScript runtime, which is the browser that you use. The JavaScript runtime uses the JavaScript engine which converts the JavaScript code to machine code. The JavaScript engine for Chrome and node is V8, and for Mozilla it's SpiderMonkey, and for Safari it's Nitro, and for Internet Explorer it's Chakra.

The JavaScript engine consists of a memory heap and a call stack. The memory heap stores all the variables defines in the JavaScript code, while the call stack contains references to the JavaScript functions and operations it needs to perform.

The JavaScript runtime provides additional features such as event listeners, HTTP / AJAX requests, timing functions, etc to support the execution of the JavaScript code.

<img width="568" alt="image" src="https://github.com/user-attachments/assets/7ebc701d-58c1-4d62-aef1-29e731357034">

## Explain the phrase "JS/node is an asynchronous non-blocking single threaded concurrent language"

JavaScript runs in a single thread in most environments, such as browsers and Node.js. This thread is responsible for executing the main JavaScript code and synchronous tasks.

JavaScript itself is single-threaded and synchronous by design, but the Web APIs provided by the browser or JavaScript runtime environment (like Node.js) enable asynchronous behavior. These APIs allow JavaScript to delegate certain tasks to the environment, freeing up the main thread to continue executing code while waiting for the completion of those tasks.

JavaScript is single threaded because it only has one call stack, which means that only one piece of code can be executed at a time.

JavaScript is also non-blocking because it doesn't wait for the response of an API call, an AJAX request or a timer, but moves on to the other parts of the code. So how is JavaScript non-blocking when it only has one thread? The asynchronous requests are performed by the web APIs in JavaScript, such as DOM API, AJAX (XMLHTTPRequest), Timeout API (setTimeout). For node, the web APIs are written in C++ and use additional C++ libraries.

Using the web APIs, concurrency is possible in JavaScript, where we can run multiple parts of the code without a multi-threaded approach.

When an asynchronous call is being made, the reference to the call is pushed to the call stack. The web API is then used to make the asynchronous call, and the asynchronous call's reference is popped out of the call stack. The call stack then can accept new requests, while the web APIs handle the asynchronous call.

The web APIs handle time-consuming operations, such as:
- Timers (e.g., setTimeout and setInterval)
- DOM Events (e.g., user clicks, keyboard events)
- Network Requests (e.g., fetch, XMLHttpRequest, or WebSockets)
- Geolocation (e.g., navigator.geolocation.getCurrentPosition)
- File Handling (e.g., FileReader API)

These APIs allow JavaScript to offload the heavy lifting, ensuring that the main thread is not blocked.

On the web API side, the web APIs handle the asynchronous request, and the callback of the asynchronous call is sent to the callback queue, which is also called the event queue. These callbacks stay on the callback queue as long as the call stack is not empty. Once the call stack becomes empty, the callback at the beginning of the callback queue is pushed to the call stack and the JavaScript engine starts executing the block of code inside the callback.

The callback queue is simply a FIFO queue where the callbacks are waiting to be invoked and moved over to the call stack.

The JavaScript runtime uses an event loop to monitor the callback queue and call stack to move asynchronous callbacks from the callback queue to the call stack once the call stack is empty.

<img width="565" alt="image" src="https://github.com/user-attachments/assets/254c5185-63fe-4303-a9e8-2498b86fdc04">

## What is the differences between fetch, promises, async/await, callbacks, event listeners, AJAX in JavaScript?

### Fetch

The fetch API is used to make asynchronous HTTP requests to a server. It returns a promise and makes it easier to handle asynchronous operations. It is also similar to the XMLHttpRequest used in AJAX.

### Promises

A promise represents a value that may be available now, later or never. Inside the promise, we can resolve or reject and return the result of the promise. It is a cleaner way to handle asynchronous operations compared to callbacks.

```js
const promise = new Promise((resolve, reject) => {
  let success = true; // Simulating a task
  if (success) resolve("Task completed!");
  else reject("Task failed!");
});

promise
  .then(result => console.log(result)) // Handles resolution
  .catch(error => console.error(error)); // Handles rejection
```

#### Promise.all

Promise.all runs multiple promises in parallel and waits for all of them to resolve. It rejects as soon as one promise fails. It's used mainly when we want to invoke calls in parallel.

```js
const p1 = Promise.resolve(10);
const p2 = Promise.resolve(20);
const p3 = Promise.reject("Error!");

Promise.all([p1, p2, p3])
  .then(results => console.log(results)) // Won't run
  .catch(error => console.error(error)); // Logs "Error!"
```

#### Promise.any

Promise.any runs multiple promises and resolves as soon as the first promise is fulfilled. It rejects only if all promises fail. It's used when we want to get the first successfull asynchronous call's result.

```js
const p1 = Promise.reject("Error 1");
const p2 = Promise.reject("Error 2");
const p3 = Promise.resolve(30);

Promise.any([p1, p2, p3])
  .then(result => console.log(result)) // Logs 30
  .catch(error => console.error(error)); // Won't run
```

#### Promise.allSettled

Promise.allSettled runs multiple promises and waits for all of them to settle, regardless of whether they resolve or reject. It will return an array describing each promise's outcome. It's used when we want the outcome of all promises (processing both successful and failed tasks).

```js
const p1 = Promise.resolve(10);
const p2 = Promise.reject("Error!");
const p3 = Promise.resolve(30);

Promise.allSettled([p1, p2, p3])
  .then(results => console.log(results));
// Logs:
// [
//   { status: "fulfilled", value: 10 },
//   { status: "rejected", reason: "Error!" },
//   { status: "fulfilled", value: 30 }
// ]
```

#### Promise.race

Promise.race runs multiple promises and resolves or rejects as soon as soon as the first promise settles (resolves or rejects). It's used when we want to get the fastest result (success or failure) and don't care about the rest.

```js
const p1 = new Promise(resolve => setTimeout(() => resolve(10), 500));
const p2 = new Promise((_, reject) => setTimeout(() => reject("Error!"), 300));

Promise.race([p1, p2])
  .then(result => console.log(result)) // Won't run
  .catch(error => console.error(error)); // Logs "Error!" (since p2 rejects first)
```

### Async/Await

Async/Await is a syntactic sugar where the code is expecting to receive and handle promises. It's used in places where the code has asynchronous behavior. 

Async declares the function in a code as asynchronous, and so it will return a promise or contain a promise inside it. 

Await waits until the promise or asynchronous call is resolved or rejected. Async/await essentially makes the code look and behave like synchronous code.

In most cases, calling the function is what starts the promise, and you only need to await it if you care about the results (or to do error handling). Use of async and await enables the use of ordinary try / catch blocks around asynchronous code.

### Top level await

### Callbacks

Callbacks are functions passed as arguments to other functions, which will be executed later. Callbacks could be declared as asynchronous or synchronous.

### Event listeners

Event listeners are used to handle events such as clicks, keypresses or mouse events asynchronously. They wait for an event to occur and execute a callback function.

```js
document.addEventListener('click', () => {
  console.log("Element clicked!");
});
```

### AJAX

AJAX is used for updating parts of a web page without reuploading the entire page. It was originally implemented using the XMLHttpRequest API. AJAX is now often replaced by fetch

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://api.example.com/data");
xhr.onload = () => {
  if (xhr.status === 200) console.log(xhr.responseText);
  else console.error("Request failed");
};
xhr.send();
```

## What is the difference between var, let and const?

Note that hoisting is done during the compilation in JavaScript. And the variables are accessed during runtime.

### var:
- Function or global scoped depending on where it is
- Re-declaration is allowed
- Re-assignment is allowed
- Hoisted to the top of the function and initialized to a default value of undefined

```js
// hoisting with var

console.log(x) // undefined

var x = 1 // variables with var are hoisted and declared with a default value of undefined
```

### let:
- Block scoped
- Re-declaration is not allowed
- Re-assignment is allowed
- Hoisted to the top of the block, but is not initialized to any default value

```js
// hoisting with let

{
  console.log(a) // causes an error since a is not initialized to any value but is hoisted
  
  let a = 5 // variables with let are hoisted but not declared with any default value
}
```

### const:
- Block scoped
- Re-declaration is not allowed
- Re-assignment is not allowed
- Hoisted to the top of the block, but is not initialized to any default value

```js
// hoisting with const

{
  console.log(b) // causes an error since b is not initialized to any value but is hoisted

  const b = 6 // variables with const are hoisted but not declared with any default value
}
```

## What is prototypal inheritance?

Every JavaScript object has an internal link to another object called its prototype (accessible via the __proto__ property in modern JavaScript or the deprecated [[Prototype]] in older terms).

If an object does not have a property or method, JavaScript automatically looks up the prototype chain until it finds the property or reaches the end of the chain (null).

An object can inherit properties and methods from another object by setting the prototype of one object to another.

Every function in JavaScript (except Arrow functions) has a prototype property, which is an object.

This prototype object is used as the prototype for objects created by the constructor function.

```js
function Person(name) {
  this.name = name;
}

Person.prototype.greet = function () {
  console.log(`Hello, my name is ${this.name}`);
};

const john = new Person("John");
john.greet(); // "Hello, my name is John"
```

The __proto__ property (or Object.getPrototypeOf(obj)) retrieves the prototype of an object.

```js
const obj = {};
console.log(obj.__proto__ === Object.prototype); // true
```

Advantages of Prototypal Inheritance

Dynamic Extension:
- Objects can inherit directly from other objects, making it easy to create flexible hierarchies.

Shared Methods:
- Methods defined on the prototype are shared across all instances, reducing memory usage.

Open for Extension:
- Prototypes can be modified at runtime, and changes are reflected in all instances.

What Is the Difference Between Prototype and Instance Properties in JavaScript?

A prototype property is a property that is defined on the prototype object of a constructor function. Instance properties are properties that are defined on individual objects that are created by a constructor function.

Prototype properties are shared by all objects that are created by a constructor function. Instance properties are not shared by other objects.

### Prototypal Inheritance in Modern JavaScript

JavaScript introduced the class syntax in ES6, which provides a more familiar, class-based interface for working with prototypal inheritance.

```js
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(`${this.name} makes a noise.`);
  }
}

class Dog extends Animal {
  speak() {
    console.log(`${this.name} barks.`);
  }
}

const dog = new Dog("Rover");
dog.speak(); // "Rover barks."
```

## What does bind do in JavaScript? What does it do for arrow functions?

The bind method in JavaScript creates a new function with a specific this context and optionally some preset arguments. This is useful for ensuring a function executes with the desired this value, regardless of how or where it is called.

The first argument to bind determines what this will refer to when the new function is invoked.

It does not call the function immediately but returns a new function that can be invoked later.

```js
const person = {
  name: "Alice",
  greet: function (greeting) {
    console.log(`${greeting}, my name is ${this.name}`);
  }
};

const unboundGreet = person.greet;
unboundGreet("Hello"); // Hello, my name is undefined (this refers to the global object or undefined in strict mode)

const boundGreet = person.greet.bind(person);
boundGreet("Hello"); // Hello, my name is Alice
```

Arrow functions behave differently from regular functions when it comes to this. Specifically:

Arrow Functions Don't Have Their Own this:
- Arrow functions inherit this from their surrounding lexical scope (the context in which they were defined).
- bind Has No Effect on Arrow Functions:
- Since the this value in an arrow function is already fixed to the lexical context, calling bind will not change it.

```js
const person = {
  name: "Alice",
  greet: () => {
    console.log(`Hello, my name is ${this.name}`);
  }
};

const boundGreet = person.greet.bind({ name: "Bob" });
boundGreet(); // Hello, my name is undefined (arrow function ignores bind)

const regularGreet = function () {
  console.log(`Hello, my name is ${this.name}`);
};
const boundRegularGreet = regularGreet.bind({ name: "Bob" });
boundRegularGreet(); // Hello, my name is Bob
```

Why Doesn't bind Work with Arrow Functions?
- Lexical Scoping: Arrow functions capture the this value from their enclosing execution context when they are defined.
- No Dynamic Binding: Unlike regular functions, arrow functions do not have their this set dynamically based on how they are called (or by using methods like bind, call, or apply).

## What are symbols in JavaScript?

A Symbol is a primitive data type introduced in ES6 (ECMAScript 2015). It is a unique and immutable value often used as an identifier for object properties. Symbols provide a way to create "hidden" or "non-colliding" properties on objects, ensuring no unintentional property name clashes.

Symbols are created using the Symbol() function. Each time you call Symbol(), a new and unique symbol is created.

```js
const sym1 = Symbol();
const sym2 = Symbol();

console.log(sym1 === sym2); // false (each symbol is unique)
```

You can also provide a description for a symbol, which is useful for debugging:

```js
const sym = Symbol("uniqueDescription");
console.log(sym); // Symbol(uniqueDescription)
```

Even if two symbols have the same description, they are guaranteed to be unique.

```js
const sym1 = Symbol("description");
const sym2 = Symbol("description");
console.log(sym1 === sym2); // false
```

Immutable:
- Once a symbol is created, its value cannot be changed.

Not Enumerable:
- Symbol properties on objects are not enumerable. They do not appear in for...in loops or Object.keys().

Hidden Properties:
- Symbols allow you to add properties to objects without affecting their public interface. This is useful for creating private or hidden properties.

Using Symbols as Object Keys
- Symbols can be used as keys for object properties to ensure property uniqueness and avoid conflicts with other keys.

```js
const sym = Symbol("id");

const obj = {
  [sym]: 123,
  name: "Alice"
};

console.log(obj[sym]); // 123
console.log(obj.name); // "Alice"
```

Accessing Symbol Properties:
- Use obj[symbol] syntax to access properties keyed by symbols.
- Symbols are not visible in Object.keys() or for...in but can be accessed using Object.getOwnPropertySymbols().

## What is the difference between function declaration and function expression?

Function declarations are defined using the function keyword, while function expressions are defined by assigning a function to a variable. Function declarations are hoisted, while function expressions are not.

```js
function multiply(a, b) {
  return a * b
}

const add = function(a, b) {
  return a * b
}

multiply(3, 5)
add(3, 5)
```

## What Is the Difference Between localStorage and sessionStorage in JavaScript?
Both localStorage and sessionStorage are web storage objects in JavaScript, but they have different scopes and lifetimes.

localStorage persists data even after the browser window is closed and is accessible across different browser tabs/windows of the same origin.
sessionStorage stores data for a single browser session and is accessible only within the same tab or window.

```js
localStorage.setItem("name", "John")
console.log(localStorage.getItem("name"))

sessionStorage.setItem("name", "John")
console.log(sessionStorage.getItem("name"))
```

## What Is a Generator Function in JavaScript?

A generator function is a special type of function that can be paused and resumed during its execution. It allows generating a sequence of values over time, using the yield keyword.

```js
function* generateNumbers() {
  yield 1
  yield 2
  yield 3
}

const generator = generateNumbers()
console.log(generator.next().value) // Output: 1
console.log(generator.next().value) // Output: 2
console.log(generator.next().value) // Output: 3
```

## Explain the concept of currying in JavaScript and how it can be implemented. Provide an example.

Currying is the process of converting a function that takes multiple arguments into a sequence of functions that each take a single argument. It can be implemented using nested functions or by using libraries like Lodash. Example:

```js
function multiply(a) {
  return function (b) {
    return a * b;
  };
}
const multiplyByTwo = multiply(2);
console.log(multiplyByTwo(3)); // Outputs: 6
```

## Explain the concept of event-driven programming in JavaScript. Provide examples of event-driven architecture in web applications.

Event-driven programming is a programming paradigm where the flow of the program is determined by events such as user actions, system events, or messages from other parts of the program. Examples in web applications include handling user interactions (clicks, keypresses), AJAX requests, and DOM manipulation.

## What is the purpose of the WeakMap and WeakSet data structures in JavaScript? How do they differ from Map and Set?
 
WeakMap and WeakSet are special types of collections in JavaScript that allow only objects as keys (for WeakMap) or values (for WeakSet). They hold weak references to objects, meaning that they do not prevent garbage collection of the objects they reference. This makes them useful for scenarios where objects should be automatically removed when they are no longer needed.

Misc notes:

```js
"use strict"

// note that node assumes a lot of things, such as assuming a field might be 
// undefined if it is not defined within an object, or that a variable is defined 
// already (when it is not) if it was declared, for example the below c=5 is 
// declared but not defined, and thus using "use strict" will cause an error, but 
// if we removed "use strict", then there would not be an error
c = 5

const z = {a: "bob"}
console.log(x + y)

// note that since the b field in the variable z doesn't exist, z.b will be undefined
console.log(`${z.b}`)

// even if z, an object is a constant, we can still change the value of it
z.b = "bobby"
console.log(z.b)

console.log(z.b.length) // returns 5

var k
console.log(k)
// by default k is undefined because it is defined but not declared

// We also want to specifically use const when importing files or modules because we don't want to change the files / modules

// below defines an empty object
var student = {}
student.firstname = "Riyaz"
student.lastname = "Sayyad"
student.age = 35
console.log(student)

// note that we can have different data types in the array
var y = [10, 20, "Riyaz", true]

// below is a for each loop in JS
y.forEach((ele) => {
  console.log(ele)
})

// note that even it we declared a using let a = 20 within the code block, the 
// var a = 10 still takes precedence outside the block because let is block scopped
var a = 10
if (true) {
  let a = 20
  console.log(a) // prints 20
}

console.log(b) // prints 10

function doStuff(data) {
  return new Promise((resolve, reject) => {

    // note that the resolve and reject can only be called once, and if 
    // they're called multiple times, then only the first call will be 
    // considered
    if (typeof data === "boolean") {
      resolve("type is boolean")
    } else {
      reject("type is not boolean")
    }
  })
}

// we can print the promise result
console.log(doStuff(true)) // prints Promise { 'type is boolean' }

// we can chain the promise as well
doStuff(true).then((res) => {
  // res will take the actual response within the resolve() call
  console.log(res) // prints type is boolean
}).catch((res) => {
  console.log(res)
})

// the first call to the promise resolved, but the second call 
// below with doStuff(123) will reject
doStuff(true).then(() => {
  console.log("First doStuff resolved")
  return doStuff(123)
}).then(() => {
  console.log("Second doStuff resolved")
}).catch(() => {
  console.log("Error occured")
})
```
