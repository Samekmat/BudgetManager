async function deleteCategory(categoryID) {
    // 1. Retrieve ID that we want to remove
    // 2. Send DELETE request to API to remove db record - TO DO
    // 3. Update DOM with removed income record
    let deleteViewEndpoint = `/api/category/${categoryID}/delete/`;
    let response = await fetch(deleteViewEndpoint, {
     method: "DELETE",
     headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
     },
      });

    console.log(response)

    let statusCode = await response.status;

    if(statusCode == 204) {
        let trToRemove = document.getElementById(`category-${categoryID}`);
        trToRemove.remove();

        location.reload();
    }


    }
