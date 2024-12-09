let logOut = document.querySelector("#logout")

if (logOut)
{

    console.log(document.cookie['user_id'])
    logOut.addEventListener("click", ()=>openPop())
    let popDisplay = document.querySelector("#popup")

    function openPop()
    {
        popDisplay.classList.remove("off")
        popDisplay.classList.add("on")
    }

    function closePop()
    {
        popDisplay.classList.remove("on")
        popDisplay.classList.add("off")

    }
    function sendLogOut()
    {
        window.location.href='/logout'
    }

}
