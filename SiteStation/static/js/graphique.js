const charts = {}, heures = {}

//Défini l'objet permettant de trouver l'heure au format "hh:mm" grâce à l'heure au format "hhmm" / "hhm" / "hmm" / "hm"
for(let h = 0; h < 24; h += 1) {
    for(let m = 0; m < 60; m += 1) {
        let cle = new String(new String(h) + new String(m))
        let cleFinale = ""
        if (cle.length === 2) {
            cleFinale = cle[0].padStart(2, "0") + cle[1].padStart(2, "0")
        } else if (cle.length === 4) {
            cleFinale = cle
        } else if (h >= 10) {
            cleFinale = cle[0] + cle[1] + cle[2].padStart(2, "0")
        } else {
            cleFinale = cle[0].padStart(2, "0") + cle[1] + cle[2]
        }
        heures[cleFinale] = new String(h).padStart(2, "0") + ":" + new String(m).padStart(2, "0")
    }
}

/**
 * Crée un graphique avec la liste des données et le type du capteur voulu.
 * @param {"humidite"|"lumiere|"pression"|"temp1"|"temp2"} type Type du capteur
 * @param {Array.<Array.<{dateDonnee: String, heure: String, typeDonnee: String, donnee: Number}>>} data Données enregistrées le jour voulu
 */
function creerGraphique(type, data) {
    //Défini la place du graphique
    let margin = {top: 20, bottom: 20, left: 40, right: 20} 
    let width = 1440 - margin.left - margin.right, height = 500 - margin.top - margin.bottom

    //Trie les données par type et les regroupe. On divise la donnée de lumière par 6 pour l'avoir environ en pourcentage.
    let donnees = data.filter(e => e[2] === type)
    let donneesEtiquetees = {
        name: type,
        values: donnees.map((donnee) => {
            let diviseur = 1
            if (type === "lumiere") {
                diviseur = 6
            }
            return {
                time: heures[donnee[1]],
                value: donnee[3] / diviseur
            }
        })
    }

    //Liste toutes les valeurs des données
    let valeurs = donneesEtiquetees.values.map((valeur) => valeur.value)

    //Crée le graphique
    var graphique = d3.select("#graphique")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
    var graph = graphique
        .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
    
    graph.append("text")
        .attr("x", width / 2)
        .attr("y", 0)
        .attr("text-anchor", "center")
        .style("font-size", "20px")
        .style("text-decoration", "bold")
        .text(TYPES[type][0] + " (en " + TYPES[type][1] + ")")
    
    var x = d3.scaleTime()
        .domain([new Date(1900, 0, 1, 0, 0), new Date(1900, 0, 2, 0, 0)])
        .range([ 0, width ]);
    graph.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(d3.timeHour.every(1)).tickFormat(d3.timeFormat("%H:%M")));

    var parseTime = d3.timeParse("%H:%M")
    var y = d3.scaleLinear()
        .domain([Math.floor(Math.min(...valeurs)), Math.ceil(Math.max(...valeurs))])
        .range([ height, 0 ]);
    
    graph.append("g")
        .call(d3.axisLeft(y))
    var line = d3.line()
        .x(function(d) { return x(parseTime(d.time)) })
        .y(function(d) { return y(d.value) })
    graph.selectAll("myLines")
        .data([donneesEtiquetees])
        .enter()
        .append("path")
            .attr("d", function(d){ return line(d.values) } )
            .style("stroke", "red")
            .style("stroke-width", 5)
            .style("fill", "none")

    //Rajoute le graphique à l'objets charts pour pouvoir choisir lequel est sélectionné
    charts[type] = graphique

    //Réinitialise la div graphique pour permettre de créer le prochain graphique
    let graphiqueHTML = document.getElementById("graphique")
    graphiqueHTML.innerHTML = ""
}

/**
 * Change le graphique choisi en fonction de l'élément cliqué
 * @param {Object} caller Élément qui appelle la fonction
 */
function menuTypeData(caller) {
    let menu = document.getElementsByClassName("menuType")
    for (var i = 0; i < menu.length; i++) {
        menu[i].classList.remove("selection")
    }
    caller.classList.add("selection")
    let graphique = document.getElementById("graphique")
    graphique.innerHTML = charts[caller.id]._groups[0][0].outerHTML
}
