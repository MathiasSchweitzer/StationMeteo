const JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
const MOIS = [
    ["Janvier", 31],
    ["Février", 28],
    ["Mars", 31],
    ["Avril", 30],
    ["Mai", 31],
    ["Juin", 30],
    ["Juillet", 31],
    ["Août", 31],
    ["Septembre", 30],
    ["Octobre", 31],
    ["Novembre", 30],
    ["Décembre", 31]
]

/**
 * Ouvre la page des données du jour
 */
function aujourdhui() {
    let date = new Date()
    open(`/${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`, "_self")
}

/**
 * Ouvre la page du mois recherché
 */
function allerA() {
    let jour = document.getElementById("rechercheJour").value, mois = document.getElementById("rechercheMois").value, annee = document.getElementById("rechercheAnnee").value
    if (annee === "") {
        return alert("L'année de recherche est invalide.")
    } else if (mois === "") {
        open(`/${annee}`, "_self")
    } else if (jour === "") {
        open(`/${annee}/${new String(mois).padStart(2, "0")}`, "_self")
    } else {
        open(`/${annee}/${new String(mois).padStart(2, "0")}/${new String(jour).padStart(2, "0")}`, "_self")
    }
}

/**
 * 
 * @param {*} e 
 */
function checkRecherche(e) {
    if (e.code === "Enter") {
        allerA()
    }
}

/**
 * Défini la fonction de la touche entrée pour rechercher après le chargement de la page
 */
function definiRecherche() {
    document.getElementById("spanRecherche").onkeydown = checkRecherche
}

/**
 * Passe à l'instance suivante, en fonction des éléments fournis
 * @param {Number} an Année actuelle
 * @param {Number} mois Mois actuel
 * @param {Number} jour Jour actuel
 */
function precedent(an, mois = null, jour = null) {
    if (mois === null) {
        open(`/${an - 1}`, "_self")
    } else if (jour === null) {
        mois -= 1
        if (mois <= 0) {
            an -= 1
            mois += 12
        }
        open(`/${an}/${new String(mois).padStart(2, "0")}`, "_self")
    } else {
        jour -= 1
        if (jour <= 0) {
            mois -= 1
            if (mois <= 0) {
                an -= 1
                mois += 12
            }
            jour += MOIS[mois - 1][1]
        }
        open(`/${an}/${new String(mois).padStart(2, "0")}/${new String(jour).padStart(2, "0")}`, "_self")
    }
}

/**
 * Passe à l'instance suivante, en fonction des éléments fournis
 * @param {Number} an Année actuelle
 * @param {Number} mois Mois actuel
 * @param {Number} jour Jour actuel
 */
function suivant(an, mois = null, jour = null) {
    if (mois === null) {
        open(`/${an + 1}`, "_self")
    } else if (jour === null) {
        mois += 1
        if (mois > 12) {
            an += 1
            mois -= 12
        }
        open(`/${an}/${new String(mois).padStart(2, "0")}`, "_self")
    } else {
        jour += 1
        if (jour > MOIS[mois - 1][1]) {
            mois += 1
            if (mois > 12) {
                an += 1
                mois -= 12
            }
            jour = 1
        }
        open(`/${an}/${new String(mois).padStart(2, "0")}/${new String(jour).padStart(2, "0")}`, "_self")
    }
}

/**
 * Ouvre une page en fonction de l'id de l'élément
 * @param {SVGTSpanElement} caller Element qui appelle la fonction
 */
function ouvrir(caller) {
    open(caller.id, "_self")
}