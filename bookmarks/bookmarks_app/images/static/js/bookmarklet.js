const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;

// load css
var head = document.getElementsByTagName('head')[0];
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'css'
link.hred = styleUrl + '?r=' + Math.floor(Math.random()*99999999999999);
head.appendChild(link);

// load html
var body = document.getElementsByTagName('body')[0];
boxHtml = 
    `<div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
</div>`;

body.innerHTML += boxHtml;

// lauch the bookmarklet 

function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');
    // clear images found 
    imagesFound.innerHTML = '';
    // display bookmarklet 
    bookmarklet.style.display = 'block';
    // close event 
    bookmarklet.querySelector('#close').addEventListener('click' , function() {
        bookmarklet.style.display = 'none'
    });
    // find images in the DOM with the minimum dimensions 
    images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"] , img[src$=".png"]');
    images.forEach(image => {
        if(image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
            var imageFound = document.body.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound)
        }
    })
}

// launch the bookmarklet
bookmarkletLaunch();