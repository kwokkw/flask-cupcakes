# Springboard - Flask Cupcake Exercise

## Table of contents

- [Springboard - Flask Cupcake Exercise](#springboard---flask-cupcake-exercise)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
    - [The challenge](#the-challenge)
    - [Links](#links)
  - [My process](#my-process)
    - [Built with](#built-with)
    - [What I learned](#what-i-learned)
    - [Continued development](#continued-development)
    - [Useful resources](#useful-resources)
  - [Author](#author)
  - [Acknowledgments](#acknowledgments)
  - [Time estimate](#time-estimate)
  - [Questions - RESTful API](#questions---restful-api)

## Overview

### The challenge

1.  Dynamically add a newly created list item.
   
    1.  Send the data to the backend
        - When the "Create/Add" button is clicked, gather the form data and send it to the backend using a `createItem()` method. 

    2.  Receive the newly created cupcake:
        - Once the backend creates the new item, it should return the item data (including the new `id`).

    3.  Update the DOM dynamically:
        - Append the new item to the list in the DOM without refreshing the page. 

### Links

## My process

### Built with

### What I learned

### Continued development

1.  Review of JS class method and instance method
   
   **Class Methods**
   Class methods are methods that are bound to the class and not the instance of the class. They can access and modify the class state that applies across all instances of the class. These methods are declared using `static` keyword. 

   **Instance Methods**
   Instance methods are methods defined within a class that operate on an instance of that class. They can access and modify the instance's properties and are called on individual objects created from the class. 

2. Review of the Axios `post` method.

- Basic syntax: `axios.post(url, data, config)`.
  - url is the endpoint where the request is sent.
  - data to be sent to the server, typically in JSON format
  - config is optional. 


### Useful resources

## Author

## Acknowledgments

## Time estimate 

## Questions - RESTful API

1. I am looking for solution and clarification on how form data is handled under the following scenario. 

   form is not being validated on server side (flask route).

     Springboard requirement: 
      
      * Refactor your front-end code to be object-oriented using class methods to `fetchAllCupcakes` and `createCupcakes` and instance methods for updating and deleting cupcakes as well as searching for cupcakes. 

      * Refactor your HTML page to render a form created by WTForms.

      - When using WTForms, what is the best practice to handle the `<form>` html elements? For example, `acction`, `method` attributes.
        - From my understanding, JavaScript intervene form submission with `addEventListener`. Is `action="/api/cupcakes"` still needed in the `form` HTML element?

   **Problem** 

   csrf token was not being sent to the server side. 

   **Solution**

   Add csrf token to JavaScript.
   [CSRF Protection](https://flask-wtf.readthedocs.io/en/1.0.x/csrf/#javascript-requests)

   To verify csrf token was not sent:

   Option 1 
   - `breakpoint()`, in `app.py`
   - `n`, next line (in code?)
   - `form.errors`, to see what error being experiencing

   Option 2
   - `Network` tab in browser 
   - `Payload`, look at the data

   **My approach**

   Use jQuery to capture and extract the csrf token and it's value, then store it in a `csrfToken` variable. Lastly, inclued the `csrfToken` in the `formData` and send it to the server side. 

2. `cupcakes.js` is not being loaded in the extended `edit-cupcake-form.html`.
   -  overriding the content in the "index.html" with the "edit-cupcake.html"