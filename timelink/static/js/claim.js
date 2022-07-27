// controller
function claimTimeLinkBot() {
    const submitClaim = document.querySelector(".btn-claim");
    submitClaim.addEventListener("click", () => {
        const claimData = document.getElementById("claim");
        const data = claimData.value;
        apiFetch.postDataToApi("claim", data).then(() => {
            claimData.value = "";
            location.reload();
        });
    });
}

claimTimeLinkBot();
