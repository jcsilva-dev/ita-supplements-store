console.log("Campaign Banner JS carregado");

const countdown = document.getElementById("campaign-countdown");

if (countdown){

    const endDate = new Date(countdown.dataset.end);

    function updateCountdown(){

        const now = new Date();

        const distance = endDate - now;

        if(distance <= 0){

            countdown.innerHTML = "Encerrada";

            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));

        const hours = Math.floor((distance % (1000*60*60*24)) / (1000*60*60));

        const minutes = Math.floor((distance % (1000*60*60)) / (1000*60));

        const seconds = Math.floor((distance % (1000*60)) / 1000);

        countdown.innerHTML =
            `${days}d ${hours}h ${minutes}m ${seconds}s`;

    }

    updateCountdown();

    setInterval(updateCountdown,1000);

}