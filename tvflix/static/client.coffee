username = localStorage.getItem("username")
apikey = localStorage.getItem ("apikey")
(($) ->
  setLogout = ->
    $('#userLoginButton').html("Logout").attr('data-logout', true)
  #Retrive the user info
  getUserInfo = ->
    username = $("#username").val()
    apikey = $("#apikey").val()

    if !username || !apikey
      $("#emptyAlert").fadeIn()
      return false
    else
      $("#emptyAlert").fadeOut();

    #Save in local storage
    localStorage.setItem("username", username)
    localStorage.setItem('apikey', apikey)
    return true

  handleLogout = ->
    username = null
    apikey = null
    localStorage.removeItem("username")
    localStorage.removeItem("apikey")
    $(this).html("Login").removeAttr('data-logout')

  if username && apikey
    setLogout()


  $("#loginButton").click (e) ->
    e.preventDefault()
    if getUserInfo()
      $("#loginModal").modal("hide")
      setLogout()

  $('#userLoginButton').click (e) ->
    e.preventDefault()
    if $(this).attr("data-logout")
      handleLogout.call(this)
    else
      $("#loginModal").modal("show")

) jQuery