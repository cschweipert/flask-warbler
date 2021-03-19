let $likeForm = $(".like-form");
let $likeButton = $(".like-button")

console.log("like button: ", $likeButton)

let buttonId = $likeButton.id

console.log("like button Id: ", buttonId)

$likeForm.on('submit', async (e) => {
    e.preventDefault();
    
    let buttonId = $(e.target).children().attr("id")
    let bId = buttonId.split("-")[1]


    let response = await axios.post(`/messages/${bId}/like`)
    $(e.target).children().toggleClass("fas", "far")
    
    console.log("Response:", response) 
})