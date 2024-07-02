$(document).ready(function() {
    var recipes = {};

    // Carregar receitas do JSON
    $.getJSON("/static/js/recipes_fit.json", function(data) {
        recipes = data;
    });

    $("#search-input").on("input", function() {
        var query = $(this).val();
        if (query.length > 0) {
            $.ajax({
                url: "/autocomplete",
                data: { q: query },
                success: function(data) {
                    var autocompleteList = $("#autocomplete-list");
                    autocompleteList.empty();
                    data.forEach(function(item) {
                        autocompleteList.append("<li class='autocomplete-item'>" + item + "</li>");
                    });
                    $(".autocomplete-item").on("click", function() {
                        $("#search-input").val($(this).text());
                        $("#autocomplete-list").empty();  // Clear suggestions
                    });
                }
            });
        } else {
            $("#autocomplete-list").empty();
        }
    });

    

    $(".search-button").on("click", function(e) {
        e.preventDefault();
        var selectedRecipe = $("#search-input").val().trim();
        if (recipes[selectedRecipe]) {
            window.location.href = recipes[selectedRecipe];
        } else {
            alert("Receita não encontrada!");
        }
    });
});
