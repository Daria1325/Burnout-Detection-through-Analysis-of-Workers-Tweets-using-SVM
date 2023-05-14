// document.getElementById('circleValue').addEventListener('change', ({ target }) => {
//     let { value: circleValue }= target;
//     if (circleValue > 100) {
//       circleValue = 100;
//     }
//     let successValue = (circleValue/100)*660;
//     document.getElementById('circle-percentage').innerHTML= `${circleValue}%`;
//     document.getElementById('success-value').setAttribute('stroke-dasharray', `${successValue}, 660`);
//   });

circles = document.getElementsByClassName('success-circle')
for (let i = 0; i < circles.length; i++) {
    circleValue = circles[i].getAttribute('percent')
    let fullValue = 2*22/7*circles[i].getAttribute('r')
    let successValue = (circleValue/100)*fullValue*0.75;
    circles[i].setAttribute('stroke-dasharray', `${successValue}, ${fullValue}`);
    if (i==0){
        circles[i].setAttribute('stroke', '#25BE4B');
    }else if (i==1){
        circles[i].setAttribute('stroke', '#BE253A');
    } else if (i==2){
        circles[i].setAttribute('stroke', '#2585BE');
    }else{
        circles[i].setAttribute('stroke', '#FFA550');
    }
}
