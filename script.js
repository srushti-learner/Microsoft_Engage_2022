

const searchWrapper = document.querySelector(".search-input")
const a = searchWrapper.querySelector("#autoComplete");
const b = searchWrapper.querySelector("#movie_list");

fetch('../static/file.json')
.then((response) =>  response.json())
.then((data)=>{
    movies = data.map((x) => x.movie_title);
    movies.sort();
    a.onkeyup=(e)=>{
        let userData = e.target.value;
        let emptyArray =[];
        if(userData){
            emptyArray = movies.filter((data)=>{
                return data.toString().toLowerCase().startsWith(userData.toLowerCase());                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
            });
            emptyArray=emptyArray.map((data)=>{
                return data = '<li>'+ data +'</li>';
            });
  
            searchWrapper.classList.add("active");
            showSuggestions(emptyArray);
            let allList = b.querySelectorAll("li");
            
            for (let i=0; i<allList.length; i++){
                allList[i].setAttribute("onClick","select(this)");
                
            }
        }
        else{
            searchWrapper.classList.remove("active");
        }
    } 
    });


    function select (element){
        let selectUserData=element.textContent;
        a.value=selectUserData;
        searchWrapper.classList.remove("active");
    }
    function showSuggestions(list){
        let listData;
        if(!list.length){
            userValue=a.value;
            listData = '<li>'+userValue+'</li>'

        }
        else if (list.length>=5){
            let maxLength = 10;
            let newArray = [];
            for (var i=0;i<maxLength;i++){
                newArray.push(list[i]);
            }
            listData = newArray.join('');
        }
        else{
            listData=list.join('');
        }
        b.innerHTML = listData;
    }




