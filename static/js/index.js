function myFunc(vars) {
    //Creamos la letiable tbody par manipular la tabla
    let tbody = document.getElementById('tbody');
    //Ingresan el número de cada afinidad desde la consulta
    let alta = vars[0];
    let media = vars[1];
    let baja = vars[2];
    var afin = [alta, media, baja]

    if (alta > 0) {
        tbody.children[0].appendChild(document.createElement("td"));
        tbody.children[0].children[3].setAttribute("rowspan", alta);
        tbody.children[0].children[3].setAttribute("align", "center");
        tbody.children[0].children[3].setAttribute("valign", "center");
        tbody.children[0].children[3].innerHTML = "Alta";
        tbody.children[0].children[3].style.backgroundColor = "#80B540";
        tbody.children[0].children[3].style.fontWeight = "bold";
    }
    if (media > 0) {
        tbody.children[alta].appendChild(document.createElement("td"));
        tbody.children[alta].children[3].setAttribute("rowspan", media);
        tbody.children[alta].children[3].setAttribute("align", "center");
        tbody.children[alta].children[3].setAttribute("valign", "center");
        tbody.children[alta].children[3].innerHTML = "Media";
        tbody.children[alta].children[3].style.backgroundColor = "#EFCD20";
        tbody.children[alta].children[3].style.fontWeight = "bold";
    }
    if (baja > 0) {
        tbody.children[alta + media].appendChild(document.createElement("td"));
        tbody.children[alta + media].children[3].setAttribute("rowspan", baja);
        tbody.children[alta + media].children[3].setAttribute("align", "center");
        tbody.children[alta + media].children[3].setAttribute("valign", "center");
        tbody.children[alta + media].children[3].innerHTML = "Baja";
        tbody.children[alta + media].children[3].style.backgroundColor = "#F1893D";
        tbody.children[alta + media].children[3].style.fontWeight = "bold";
    }
}


for(var i = 0; i < document.getElementsByClassName('score').length; i++){
    document.getElementsByClassName('score')[i].innerHTML = document.getElementsByClassName('score')[i].innerHTML.substring(0,5)
}