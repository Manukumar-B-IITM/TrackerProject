function validateForm() {

}

function myTracketTypeSelect() {
    if (document.getElementById("ttype").value === "2") {
        document.getElementById("trackersettings").classList.remove("hideTrackerSettings")
    } else {
        document.getElementById("trackersettings").classList.add("hideTrackerSettings")
    }
}

function validateTrackerData() {
    // let d = 

    let x = document.forms["create-tracker-form"]["t_type"].value;
    if (x == "2") {
        let s = document.forms["create-tracker-form"]["tsettings"].value;
        if (s == "") {
            alert("Setting values missing for multiple choice.")
            return false
        }
    }
    return true;
}

function onLoadLog() {
    document.getElementById("whenDateTime").addEventListener('change', (event) => {
        const res = document.getElementById('utctime');
        res.value = new Date(`${event.target.value}`).toISOString();
      });

    var local = new Date();
    document.getElementById('utctime').value = local.toISOString();
    local.setMinutes(local.getMinutes() - local.getTimezoneOffset());
    document.getElementById("whenDateTime").value = local.toJSON().slice(0,16);

   
}

function onLoadHome(){
    tlinks = document.querySelectorAll(".tracker-links")
    for(t in tlinks){
        tlinks[t].href += `?offset=${new Date().getTimezoneOffset()}`; 
    }
}

function validateTrackerData() {
    return true;
}