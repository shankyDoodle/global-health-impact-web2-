function capitalizeText(text) {

    return text
        .split(' ')
        .map(
            (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        ).join('');
}

// this must be updated when a new disease is added. sorry :(
// can't do if short word length since HIV/AIDS is long, for example
Array.from(document.getElementsByClassName('capitalize-first-letter'))
    .forEach(function(elt) {

        const disease = elt.textContent;
        let diseaseCased = disease;

        // console.log("disease", disease);

        switch(disease.toLowerCase()) {
            case "malaria":
                diseaseCased = capitalizeText(disease)
                break;
            case "tb":
                diseaseCased = disease.toUpperCase();
            break;
            case "hiv/aids":
                diseaseCased = disease.toUpperCase();
                break;
            case "onchocerciasis":
                // console.log("ppp");
                diseaseCased = capitalizeText(disease);
                break;
            case "schistosomiasis":
                diseaseCased = capitalizeText(disease);
                break;
            case "lf":
                diseaseCased = disease.toUpperCase();
                break;
            case "hookworm":
                diseaseCased = capitalizeText(disease);
                break;
            case "roundworm":
                diseaseCased = capitalizeText(disease);
                break;
            case "whipworm":
                diseaseCased = capitalizeText(disease);
                break;
        }

        // console.log("here", disease, diseaseCased);
        elt.textContent = diseaseCased;
    });