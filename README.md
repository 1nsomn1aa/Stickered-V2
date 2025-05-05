![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/stickeredlogo.png)

# Stickered

Stickered is a full-stack eCommerce web application built using Django and Bootstrap, designed for selling custom vehicle-themed stickers, windshield banners and license plates. The site replicates the functionality of a modern online store including customer account handling, product management, responsive UI, Stripe payments, and content control through both Front-End and Django admin interface.

[Link to Stickered on Heroku](https://stickered-9f7c00b2095b.herokuapp.com/)

---

## Table of Contents

1. [Project Goals](#project-goals)  
2. [UX Design](#ux-design)  
   - [Skeleton](#skeleton)  
   - [Surface](#surface)  
   - [Typography & Colour](#typography--colour)  
3. [Features](#features)  
   - [Front-End Features](#front-end-features)  
   - [Admin / Backend Features](#admin--backend-features)  
4. [Pages Overview](#pages-overview)  
   - [Home Page](#home-page)  
   - [Shop Page](#shop-page)  
   - [Product Detail Page](#product-detail-page)  
   - [Product Add Page](#product-add-page)  
   - [Product Edit Page](#product-edit-page)  
   - [Cart Page](#cart-page)  
   - [Checkout Page](#checkout-page)  
   - [Profile Page](#profile-page)  
   - [Order Detail Page](#order-detail-page)  
   - [Login, Register & Password Reset](#login-register--password-reset)  
   - [Contact Page](#contact-page)  
   - [About Page](#about-page)  
   - [Custom 400, 403, 404, 500 error handling pages](#custom-400-403-404-500-error-handling-pages)  
5. [Database Design](#database-design)  
6. [Technologies Used](#technologies-used)  
7. [Testing & Bugs](#testing--bugs)  
8. [Development Process](#development-process)  
9. [Deployment](#deployment)  
10. [Marketing Strategy](#marketing-strategy)  
11. [Business Model](#business-model)  
12. [Credits](#credits)

---

## Project Goals
- Build a functional online store using Django, Bootstrap and PostgreSQL.
- Provide a clean, responsive UI and intuitive UX.
- Support multiple product variations (sizes, pricing).
- Allow user registration and order tracking.
- Enable secure payments via Stripe.
- Create a maintainable codebase with admin functionality.
- Make the products section editable from the front-end.

---

## UX Design

#### Homepage
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/homedesktop.png)

The design of this project was kept simple yet modern to make the site easy to use, but still pleasing to look at. Since the product images are bright and colorful, the rest of the site uses mostly black (#000000), dark gray (#55595c), and a soft off-white blue (#f0f8ff). These neutral colors help the products stand out. A bold red (#dc3545) is used for buttons and important messages. Overall, the result is clean and clear, without any unnecessary distractions.

### Skeleton
Wireframe for the home page was drafted using Balsamiq and was used throughout the development process.

#### Balsamiq Homepage
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/testing/design.png)

### Surface
- Uses Bootstrap 5 for consistent styling.
- Swiper JS for responsive slides.
- Soft borders, neutral grays, and highlight colors for a clean aesthetic.
- Buttons and navigation items with a high contrast ratio which makes them easy to see.

### Typography & Colour
- **Font:** The website uses two fonts - "Russo One" and "Funnel Display". Russo is used on large heading and Funnel is used on smaller headings and paragraphs.

#### Google Fonts
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/fonts.png)

- **Color palette:**
  - Soft White-Blue (`#f0f8ff`) and Dark Gray (`#55595c`) for backgrounds
  - Pure Black (`#000000`) and Pure White (`#FFFFFF`) for headings and emphasis
  - Bright Red (`#dc3545`) for alerts, errors, buttons and key highlights

#### Colors
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/colors.png)

---

## Features

### Front-End Features

- Fully responsive layout using Bootstrap Grid

- Navigation bar with dropdown menus and live cart item and price counter

- Product listing with sorting and filtering

- Search function to search available products by the provided keyword

- AJAX cart: add, update, remove products without reloading the page

- Checkout with billing/shipping form and shipping method selector

- Stripe payment integration

- Order confirmation and success page

- Automated emails for order status changes, contact form and password reset

- Custom profile dashboard with image upload, order and message history

- Password reset, update info, and change email features

- Contact form with automated confirmation email

- Pre-filled forms using users profile information

- Adding, Editing and Deleting products

### Admin / Backend Features

- Add/edit/delete products, categories, and size/price options

- View customer orders with status update form and tracking field

- Email system triggers different notifications based on order status

- Image upload with EXIF auto-rotation and automatic old image deletion

- Logging and error handling for cart and Stripe webhook issues

---

## Pages Overview

### Home Page
Landing page that introduces the brand. Features a large, eye-catching hero picture that sets the theme with bold information text and two buttons. After a small delay, a newsletter popup appears suggesting the users to sign up to the newsletter. After a user signs up, the information is stored and the popup no longer appears. Below is the "Latest Releases" slider by Swiper JS that shows the latest products added to the shop. Towards the bottom of the page there is a testimonial section that shows previous testimonials and a submit form that is only accessible to authenticated users and has form validation. At the bottom of the page there is a footer section with social media links.

#### Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/homedesktop.png)

#### Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/homemobile.png)

#### Mobile Navigation
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/navmobile.png)

#### Newsletter Deskop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/newsletterdesktop.png)

#### Newsletter Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/newslettermobile.png)

#### Latest Releases
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/latestreleases.gif)

#### Testimonials
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/testimonials.png)

### Shop Page
A dynamic catalog displaying all products, organized by filtering and sorting systems. Also includes the ability to search by keywords. If active filters or a specific search keyword doesn't find a match, the page displays a message with no results found. Administrators also have additional buttons for adding, editing or deleting products on the front-end.

#### Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/shopdesktop.png)

#### Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/shopmobile.png)

#### Admin
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/shopadmin.png)

#### Filter/Sort Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/filterdesktop.png)

#### Filter/Sort Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/filtermobile.png)

#### No Products Found Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/noproductdesktop.png)

#### No Products Found Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/noproductmobile.png)

### Product Detail Page
Each product features its image, title, description, size guide, usage guide and available sizes with quantity selection. Based on size and quantity, the total price updates and the correct amount is submitted when pressed on the Add to Cart button. The sidebar has product suggestions based on the current product's category.

#### Product Details Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/proddetail.gif)

### Product Add Page
Front-end form for Administrators to add a new product. Allows total control over the front-end form to provide the name, description, size guide, usage guide, select available sizes and set individual pricing.

#### Adding Products (Zoomed Out View)
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/addproduct.png)

### Product Edit Page
Front-end form for Administrators to edit current products. Edit the name, description, size guide, usage guide, change available sizes or update individual pricing.

#### Editing Products (Zoomed Out View)
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/editproduct.png)

### Cart Page
Displays items in the user’s cart with quantity controls, size info, and pricing. Features AJAX behavior.

#### Cart Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/cartdesktop.png)

#### Cart Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/cartmobile.png)

### Checkout Page
Secure checkout form, pre-filled for registered users with their information for shipping/billing. The page also displays cart summary, shipping options and Stripe payment integration. Shipping options pricing changes based on the most expensive shipping option category, for orders over 50 euro, standard shipping becomes free.

#### Checkout Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/checkoutdesktop.png)

#### Checkout Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/checkoutmobile.png)

### Profile Page
User dashboard with editable profile details, photo upload, order status tracking and previous contact messages.

#### Profile Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/profile.gif)

### Order Detail Page
Detailed breakdown of each order including items, sizes, shipping method, and current status.

#### Order Details Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/ordersummary.png)

### Login, Register & Password Reset
Uses Django Allauth with custom styling. Allauth pages customized with Bootstrap and validation messages.

#### Login Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/logindesktop.png)

#### Login Mobile
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/loginmobile.png)

### Contact Page
Form for users to submit inquiries. Messages sent via SMTP to the site owner, also saved in admin interface and user profile messages section. Includes an Iframe of google maps and a live status of store opening times.

#### Contact Us Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/contact.png)

### About Page
Describes the purpose and backstory of the site, includes an image gallery with pictures of our products being used by customers.

#### About Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/about.gif)

### Custom 400, 403, 404, 500 error handling pages
Shows custom pages for each type of error.

#### 404 Desktop
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/404.png)

---

## Database Design

Initially, SQLite was used as the database provided by Django but later migrated to PostgreSQL which was used as the main database.

#### Database Schema
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/testing/dbschema.png)

---

## Technologies Used

- Python 3
- Django 4
- PostgreSQL
- Stripe Payments
- Django Allauth
- AWS S3 (media storage)
- Gunicorn
- Bootstrap 5 / HTML5 / CSS3 / JavaScript
- Pillow
- Heroku
- Swiper JS

---

## Testing & Bugs

For all testing and bugs please refer to the [TESTING.md](https://github.com/1nsomn1aa/Stickered-V2/blob/main/TESTING.md) file.

---

## Development Process
This project followed an **Agile methodology**, with development broken into 10 key milestones (Epics), each focused on a major area of the site:

1. Project Setup

2. Pages & Navigation

3. Authentication

4. Product Management

5. Cart & Checkout

6. Payments

7. Media Hosting

8. Styling Polish

9. Testing

10. Deployment

To manage the workflow, I used GitHub Projects as an Agile board. I set up templates for epics and user stories, each with clear labels and priorities using the MoSCoW method (Must have, Should have, Could have, Won’t have). This helped me plan weekly tasks, keep track of progress, and focus on building features in the right order.

[GitHub Project Board](https://github.com/users/1nsomn1aa/projects/3)

![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/project.png)

[GitHub Issues: Epics and User Stories](https://github.com/1nsomn1aa/Stickered-V2/issues)

![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/readmeimages/issues.png)

---

## Deployment

The project is hosted on **Heroku**, with the following setup:
- AWS S3 bucket for image and static file storage
- Stripe live/test keys handled via config vars
- Heroku PostgreSQL as the primary database
- Heroku Config Vars to hide sensitive information

The steps I took to deploy on heroku are outlined below. 

- [x] Create a Heroku Account
- [x] Sign up at Heroku if you don’t already have an account.
- [x] Install the Heroku CLI (Optional)
- [x] Download and install the Heroku Command Line Interface (CLI) from Heroku CLI for additional control if needed.
- [x] Create a New Heroku App
- [x] Log in to your Heroku dashboard.
- [x] Click the “New” button, then select “Create New App.”
- [x] Enter an app name (unique across Heroku) and choose your region.
- [x] Connect Heroku to Your GitHub Repository
- [x] Navigate to the Deploy tab in your Heroku app dashboard.
- [x] Under Deployment Method, select GitHub.
- [x] Authorize Heroku to access your GitHub account, if prompted.
- [x] Search for and select your GitHub repository.
- [x] Enable Automatic Deploys (Optional)
- [x] In the Automatic Deploys section, click Enable Automatic Deploys if you want Heroku to deploy every time you push changes to the main branch.
- [x] Deploy Your App
- [x] To deploy manually, scroll down to the Manual Deploy section.
- [x] Select the branch you want to deploy from (e.g., main) and click Deploy Branch.
- [x] Check Your App
- [x] Once deployed, click Open App at the top-right corner of the dashboard to view your app live.
- [x] Set Environment Variables (Optional)
- [x] If your app requires environment variables (e.g., API keys), go to the Settings tab in Heroku.
- [x] Click Reveal Config Vars and add your variables in the form of key-value pairs.

Live Site: [Stickered on Heroku](https://stickered-9f7c00b2095b.herokuapp.com)

---

## Marketing Strategy

To help promote Stickered and reach more people, I created social media pages on **Facebook** and **Instagram**. These accounts are used to post product photos, share news, and connect with the car enthusiast community. Since the products are very visual, Instagram works great for showing them off, while Facebook is helpful for updates and chatting with customers.

#### Facebook
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/testing/facebook.png)

#### Instagram
![image](https://raw.githubusercontent.com/1nsomn1aa/Stickered-V2/refs/heads/main/testing/instagram.png)

Links to the pages can be found on the website's footer.

---

## Business Model

Stickered is a small online shop that follows a Business-to-Consumer (B2C) model. It sells custom stickers, license plates, and windshield banners directly to customers through the website. All items are made to order, so people can pick the size and style they want.

Running the store this way has a few benefits:

- I can control prices and make updates whenever I need  
- It's easy to add new designs or change existing ones  
- I get to talk directly with customers if they need help  
- It keeps everything simple without using third-party sellers  

Right now, the shop is aimed at individual buyers, but I might look into bulk or business orders later on if it grows.

---

## Credits

**Images**
- Logo has been created using Photoshop.
- All content related pictures were taken by me.
- All product pictures were created by me using Photoshop.
- Default profile picture was taken from [freepik](https://www.freepik.com) .
- Trust rating shield SVG was taken from [DoneDeal](https://www.donedeal.ie)

**Other Resources**

- HTML/CSS/JS/PYTHON questions [W3Schools](https://www.w3schools.com/), [freecodecamp](https://freecodecamp.org/) and my previous [GitHub Projects](https://1nsomn1aa.github.io/)
- Django Project Set-Up help from Code Institute's "Boutique Ado" demo project.
- Icons [FontAwesome](https://www.fontawesome.com/)
- Fonts [GoogleFonts](https://www.fonts.google.com/)
- Code Editor [VSCode](https://www.vscode.com/)
- Cloud Storage [GitHub](https://github.com/)
- Deployment [Heroku](https://www.heroku.com/)
- Storage [Amazon AWS](https://www.aws.amazon.com/)
- Payments [Stripe](https://www.stripe.com/)
- Validation [W3C HTML](https://validator.w3.org/) , [W3C CSS](https://jigsaw.w3.org/css-validator/) , [JSHint](https://jshint.com/) and [CI Python Linter](https://pep8ci.herokuapp.com/).
- Various forums, YouTube videos and Docs for help with how to approach specific challenges.

---