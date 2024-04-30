const inputs = [...document.querySelectorAll(".otp-box input[type='text']")];
const submitBtn = document.querySelector(".otp-box input[type='submit']");

inputs.forEach((input, index) => {
    input.addEventListener("input", (e) => {
        const value = e.target.value;
        
        if (isNaN(value) || value.length !== 1) {
            e.target.value = "";
            return;
        }

        if (index < inputs.length - 1) {
            inputs[index + 1].focus();
        }

        const isDisableBtn = inputs.some(e => e.value.length !== 1);
        submitBtn.disabled = isDisableBtn;
    });
});
