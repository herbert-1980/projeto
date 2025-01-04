document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            console.log('Botão de login clicado!');
        });
    } else {
        console.error('Elemento loginBtn não encontrado.');
    }
});


    // Alternar visibilidade da senha
    function togglePassword(inputId, button) {
        const input = document.getElementById(inputId);
        const icon = button.querySelector('i');

        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('bi-eye', 'bi-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('bi-eye-slash', 'bi-eye');
        }
    }

    // Verificar força da senha
    document.addEventListener('DOMContentLoaded', () => {
        const passwordField = document.getElementById('password1');
        const strengthIndicator = document.getElementById('password-strength');
    
        if (passwordField && strengthIndicator) {
            passwordField.addEventListener('input', () => {
                const password = passwordField.value;
                let strength = 'Fraca';
                let color = 'text-danger';
    
                if (password.length > 7 && /[A-Z]/.test(password) && /[0-9]/.test(password) && /[@$!%*?&]/.test(password)) {
                    strength = 'Forte';
                    color = 'text-success';
                } else if (password.length > 5 && /[A-Z]/.test(password) && /[0-9]/.test(password)) {
                    strength = 'Média';
                    color = 'text-warning';
                }
    
                strengthIndicator.textContent = `Força da senha: ${strength}`;
                strengthIndicator.className = color;
            });
        } else {
            console.error('Os elementos passwordField ou strengthIndicator não foram encontrados.');
        }
    });
    
