// static/js/cronometro.js
window.onload = function() {
    var timerElement = document.getElementById('time-display');
    var button = document.getElementById('start-pause-button');
    var buttonLabel = document.getElementById('button-label');
    var cronometroSection = document.querySelector('.cronometro');
    var time = parseInt(cronometroSection.getAttribute('data-time')); // Tempo inicial baseado no atributo de dados
    var timerInterval;
    var isRunning = false;

    function updateTimer() {
        var hours = Math.floor(time / 3600);
        var minutes = Math.floor((time % 3600) / 60);
        var seconds = time % 60;

        timerElement.textContent = 
            (hours < 10 ? '0' + hours : hours) + ':' +
            (minutes < 10 ? '0' + minutes : minutes) + ':' +
            (seconds < 10 ? '0' + seconds : seconds);

        if (time > 0) {
            time--;
        } else {
            clearInterval(timerInterval);
        }
    }

    function startTimer() {
        timerInterval = setInterval(updateTimer, 1000);
    }

    function pauseTimer() {
        clearInterval(timerInterval);
    }

    button.addEventListener('click', function() {
        if (isRunning) {
            pauseTimer();
            buttonLabel.textContent = 'Iniciar';
        } else {
            startTimer();
            buttonLabel.textContent = 'Pausar';
        }
        isRunning = !isRunning;
    });
}
