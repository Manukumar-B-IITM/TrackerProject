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
    let x = document.forms["create-tracker-form"]["t_type"].value;
    if (x == "2") {
        let s = document.forms["create-tracker-form"]["tsettings"].value;
        if( s == ""){
            alert("Setting values missing for multiple choice.")
            return false
        }
    }
    return true;
}