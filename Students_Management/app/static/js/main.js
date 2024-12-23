// Toggle dark mode
        document.getElementById('darkModeToggle').addEventListener('click', function () {
            const body = document.body;
            const header = document.header;
            const footer = document.footer;

            body.classList.toggle('bg-dark');
            body.classList.toggle('text-red');
            header.classList.toggle('bg-dark');
            header.classList.toggle('text-white');
            footer.classList.toggle('bg-dark');
        });