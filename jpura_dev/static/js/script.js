// // Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });


let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

if (alertWrapper) {
  alertClose.addEventListener('click', () =>
    alertWrapper.style.display = 'none'
  )
}


let searchForm = document.getElementById('searchForm') // index and projects
let pageLinks = document.getElementsByClassName('page-link')

//ensure search form exists...
if(searchForm){
  for(let i = 0; pageLinks.length > i; i++){
    pageLinks[i].addEventListener('click', clickFunc)

    function clickFunc(e){
      e.preventDefault()

      //add custom attribute to our pagination 'page'

      //get that page value || this = current button we click...
      let page = this.dataset.page

      //add hidden (attribute + value) to search form
      searchForm.innerHTML += `<input value=${page} name ='page' hidden>`

      //submit the search form
      searchForm.submit()
    }
  }
}