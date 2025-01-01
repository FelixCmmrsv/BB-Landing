function loadLanguage(language) {
    fetch(`/static/language/${language}.json`)
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll('[data-i18n]').forEach(element => {
                const key = element.getAttribute('data-i18n');
                const translation = key.split('.').reduce((obj, i) => obj?.[i], data);
                if (translation) element.innerText = translation;
            });
            document.querySelectorAll('[data-i18n-title]').forEach(element => {
                const key = element.getAttribute('data-i18n-title');
                const translation = key.split('.').reduce((obj, i) => obj?.[i], data);
                if (translation) element.title = translation;
            });
            document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
                const key = element.getAttribute('data-i18n-placeholder');
                const translation = key.split('.').reduce((obj, i) => obj?.[i], data);
                if (translation) element.placeholder = translation;
            });
            document.querySelectorAll('a[data-i18n]').forEach(element => {
                const key = element.getAttribute('data-i18n');
                const translation = key.split('.').reduce((obj, i) => obj?.[i], data);
                if (translation) element.innerText = translation;
            });
        })
        .catch(error => console.error('Error loading language file:', error));
}

function setLanguage(language) {
    loadLanguage(language);
    updateLanguageDisplay(language);
    localStorage.setItem('selectedLanguage', language);
}

function updateLanguageDisplay(language) {
    const dropdownToggle = document.querySelector('.language-dropdown .dropdown-toggle span');
    if (dropdownToggle) {
        dropdownToggle.innerText = language.toUpperCase();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    setLanguage(savedLanguage);

    const dropdown = document.querySelector('.language-dropdown');
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');

    toggle.addEventListener('click', () => {
        const isVisible = menu.style.display === 'block';
        menu.style.display = isVisible ? 'none' : 'block';
    });

    menu.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            const selectedLang = event.target.getAttribute('data-lang');
            setLanguage(selectedLang);
            menu.style.display = 'none';
        }
    });

    document.addEventListener('click', (event) => {
        if (!dropdown.contains(event.target)) {
            menu.style.display = 'none';
        }
    });
});