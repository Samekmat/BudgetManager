async function deleteTag(tagID) {
    // 1. Retrieve ID that we want to remove
    // 2. Send DELETE request to API to remove db record
    // 3. Update DOM with removed income record
    // let deleteViewEndpoint = `/api/tags/${tagID}/delete/`;
    let deleteViewEndpoint = `http://budgetm-env.eba-m8je3cyb.eu-central-1.elasticbeanstalk.com/api/tags/${tagID}/delete/`;
    let response = await fetch(deleteViewEndpoint, {
     method: "DELETE",
     headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
     },
      });

    console.log(response)

    let statusCode = response.status;

    if(statusCode === 204) {
        let trToRemove = document.getElementById(`tag-${tagID}`);
        if (trToRemove) {
        trToRemove.remove();
        }

        location.reload();
    }


    }
