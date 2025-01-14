const changeActiveLink = (link) => {
    const navItems = document.querySelectorAll('nav a');
    navItems.forEach(item => {
        if (item.id === link) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
};