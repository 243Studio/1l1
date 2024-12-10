x = document.querySelector("#custom-slug")
char_numb = document.querySelector("#char-numb")

x.addEventListener("change", printV)


function printV(e)
{
    console.log(x.value.length)
    if(x.value.length > 0)
    {
        char_numb.required = false
        console.log("Not required")
    }
    else{
        char_numb.required = true
        console.log("required")
    }
}
