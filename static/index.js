$('.material-symbols-rounded:last-child').on("click",function like(){
    try {
        axios.post(`/add_like/${$(this).data("id")}`, {
            post_id: `${$(this).data("id")}`
          })
          .then(function (response) {
            console.log(response);
          })
        
    } catch (error) {
        console.log(error)
    }
    $(this).data("id")
    $(this).toggleClass("fill")

})


