/*javascript file for autocomplete search */
//Get the input and output fields 
const searchWrapper = document.querySelector(".search-input")
const a = searchWrapper.querySelector("#autoComplete");
const b = searchWrapper.querySelector("#movie_list");

fetch('../static/file.json')/*fetching the file with movie_titles in json format */
.then((response) =>  response.json() )
.then((data)=>{
    movies = data.map((x) => x.movie_title);
    movies.sort();
    a.onkeyup=(e)=>{
        let userData = e.target.value;
        let emptyArray =[];
        if(userData){
            emptyArray = movies.filter((data)=>{
                return data.toString().toLowerCase().includes(userData.toLowerCase());                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
            });
            emptyArray=emptyArray.map((data)=>{
                return data = '<li>'+ data +'</li>';
            });
  
            searchWrapper.classList.add("active");
            showSuggestions(emptyArray);
            let allList = b.querySelectorAll("li");
            
            for (let i=0; i<allList.length; i++){
                allList[i].setAttribute("onClick","select(this)");/*adds onclick feature to the list elements*/
                
            }
        }
        else{
            searchWrapper.classList.remove("active");
        }
    } 
    });


    function select (element){ /*function which enables selection of li elements*/
        let selectUserData=element.textContent;
        a.value=selectUserData;
        searchWrapper.classList.remove("active");
    }

    function showSuggestions(list){
        let listData;
        if (list.length>=5){
            let maxLength = 20;/*showing maximum 20 suggestions*/
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