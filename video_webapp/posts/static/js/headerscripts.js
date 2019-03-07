// This is a collection of scripts that are loaded in the header

/*
  Handles display toggling
  'Button' is the id of the html element
*/
function hide(button){
  var x = document.getElementById(button);
  if (x) {
    x.style.display = "none";
  }
}

function show(button) {
  var x = document.getElementById(button);
  if (x) {
    x.style.display = "block";
  }
}

function hideToggle(button) {
  var x = document.getElementById(button);
  if (x) {
    if (x.style.display === "none") {
      show(button)
    } else {
      hide(button)
    }
  }
}

function hideToggleDual(button1, button2) {
  hideToggle(button1)
  hideToggle(button2)
}

/*
  Handles AJAX calls for:
  - Form submission
  - Pagination
*/
$(function(){
  /****** AJAX forms ******/

  // Catches a form submit for a new comment
  $(document).on("submit", ".create-comment-form", function(event) {
    console.log("Create Form Submitted")
    event.preventDefault()
    hideToggleDual('newcomment-toggle-button1','newcomment-toggle-button2') // Hide the new comment button
    data = $(this).serialize() + '&' + this.name + "=" + $(this).attr('value')
    ajaxFormSubmit(data)
  })

  // Catches a form submit for updating a comment
  $(document).on("submit", ".update-comment-form", function(event) {
    console.log("Update Form Submitted")
    event.preventDefault()
    data = $(this).serialize() + '&' + this.name + "=" + $(this).attr('value')
    ajaxFormSubmit(data)
  })

  // Catches a form submit for deleting a comment
  $(document).on("submit", ".delete-comment-form", function(event) {
    console.log("Delete Form Submitted")
    event.preventDefault()
    data = $(this).serialize() + '&' + this.name + "=" + $(this).attr('value')
    ajaxFormSubmit(data)
  })

  // Sumbits the provided data
  function ajaxFormSubmit(data) {
    $.ajax({
      method: "POST",
      url: window.location.href, // Data is sent to current page,
      // Append the form data to the POST request
      data: data,
      success: handleFormSuccess,
      error: handleFormError,
    })
  }

  // Reloads the comment section only
  function reloadComments() {
    $.ajax({
      method: 'GET',
      url: window.location.href,
      dataType : 'json',
      data: {},
      success: function(data){
        console.log("Reload success")
        $('#comment-list').replaceWith($('#comment-list',data['content']));
      },
      error: function(error){
        console.log(error);
        console.log("comment list error");
      }
    });
  }

  // Called after receiving success from server
  function handleFormSuccess(data, textStatus, jqXHR){
    // reset form data, may not be needed with reload
    $('.create-comment-form')[0].reset(); 
    $('.update-comment-form')[0].reset();
    $('.delete-comment-form')[0].reset();

    reloadComments()
  }
  
  // Called after receiving error from server
  function handleFormError(jqXHR, textStatus, errorThrown){
    console.log(jqXHR)
    console.log(textStatus)
    console.log(errorThrown)
  }

  /****** AJAX pagination ******/

  // Detects button presses in pagination section
  // Catches and sends the requested page number
  $(document).on("click", '.comment-pagination .pag-button', function(event) {
    event.preventDefault();
    url = ($('.comment-pagination .pag-button')[0].href);
    ajaxPagination($(this).attr('value'));
  });

  // Handles a pagination request for the provided page
  function ajaxPagination(page_num){
    console.log("Pagination pressed")
    // Get new data
    $.ajax({
      method: 'GET',
      url: window.location.href,
      dataType : 'json',
      data: {
        page : page_num
      },
      success: function(data){
        console.log("Pagination success")
        $('#comment-list').replaceWith($('#comment-list',data['content']));
      },
      error: function(error){
        console.log(error);
        console.log("comment list error");
      }
    });
  } 
})
