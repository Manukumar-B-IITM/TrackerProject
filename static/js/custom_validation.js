function validateForm(){
    
}

function myTracketTypeSelect(){
    if(document.getElementById("ttype").value === "2") {
        document.getElementById("trackersettings").classList.remove("hideTrackerSettings")
    } else {
        document.getElementById("trackersettings").classList.add("hideTrackerSettings")
    }
}