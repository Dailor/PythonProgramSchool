var timers = {};

function start_timer(timerKey, timerCountDown, identify){
    timers[timerKey] = {};
    timers[timerKey].countDownDate = timerCountDown;
    timers[timerKey].timer = setInterval(function() {

      // Get today's date and time
      var now = new Date().getTime();

      // Find the distance between now and the count down date
      var distance = timers[timerKey].countDownDate - now;

      // Time calculations for days, hours, minutes and seconds
      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      // Display the result in the element with id="demo"
      document.getElementById(identify).innerHTML = days + "дн " + hours + "ч "
      + minutes + "м " + seconds + "с ";

      // If the count down is finished, write some text
      if (distance < 0) {
        clearInterval(timers[timerKey].timer);
        document.getElementById(identify).innerHTML = "0дн 0ч 0м 0с";
      }
    }, 1000);
}