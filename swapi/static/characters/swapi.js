$(document).ready(function() {
    var page = 1;
    var isLoading = false;
  
    $('#load-more-btn').click(function() {
      if (isLoading) {
        return;
      }
      isLoading = true;
  
      // Show a loading spinner
      $('#load-more-btn').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...');
  
      // Make an AJAX request to fetch more data
      $.ajax({
        url: '/api/characters/',
        data: {
          page: page + 1
        },
        success: function(data) {
          // Hide the loading spinner
          $('#load-more-btn').html('Load more');
          isLoading = false;
  
          // Append the new data to the table
          var html = '';
          for (var i = 0; i < data.characters.length; i++) {
            var character = data.characters[i];
            html += '<tr>';
            html += '<td>' + character.name + '</td>';
            html += '<td>' + character.birth_year + '</td>';
            html += '<td>' + character.gender + '</td>';
            html += '<td>' + character.homeworld + '</td>';
            html += '<td>' + character.date + '</td>';
            html += '</tr>';
          }
          $('#table-body').append(html);
  
          // Increment the page counter
          page++;
        },
        error: function() {
          alert('Failed to load more data.');
          // Hide the loading spinner
          $('#load-more-btn').html('Load more');
          isLoading = false;
        }
      });
    });
  });
  