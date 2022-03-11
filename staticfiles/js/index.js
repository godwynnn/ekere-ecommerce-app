// // var i= 0;
// // let img_array=document.getElementsByClassName("intro");
// var counter=0;

// function indexslider(){
//     img_array=document.getElementsByClassName("intro");
//     for(i=0; i < img_array.length;i++){
//         img_array[i].style.display= "none";
//         }
//     counter++;
//     if (counter > img_array.length){
//         counter=1;
//     }
//     img_array[counter - 1].style.display= "block"
//     setTimeout(indexslider,1000)
// }

// // function load(){
// //     indexslider();
// // }
// // load()
// window.onload=indexslider();


// function indexslider(){
//     img_array=document.getElementsByClassName("intro");
//     for (var i in img_array){
//         if (i <= img_array.length){
//             i++;
//         }
//         else{
//             i=0
//         }
//     }
//     return img_array[i]
// }



// function iteratearray(arr){
//     for (i=0,i<arr.length;i++){
//         if (i>arr.length){
//             i=1
//         }
//         return arr[i]

//     }
// }