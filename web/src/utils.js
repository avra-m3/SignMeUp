function handleFetchErrors(response) {
    if (response.ok) {
        return response.json()
    }
    throw Error(response.status);
}


export {handleFetchErrors}