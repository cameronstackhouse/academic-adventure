window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#navbarButton'); //Assigns the button with the ID navbarButton to variable sidebarToggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => { //Listens to when the nav button is clicked 
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled'); //Toggles the sb-sidenav-toggled class on the navbar container to allow the css to transition in and out of the page
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});
