document.addEventListener('DOMContentLoaded', function () {
    const addReceiverBtn = document.getElementById('addReceiverBtn');
    const receiversList = document.getElementById('receiversList');
    const changeEmailBtn = document.getElementById('changeEmailBtn');
    const emailPopup = document.getElementById('emailPopup');
    const closePopupBtn = document.getElementById('closePopupBtn');
    const changeEmailForm = document.getElementById('changeEmailForm');

    
    const bulkEmailBtn = document.getElementById('bulkEmailBtn');
    const scheduleEmailBtn = document.getElementById('scheduleEmailBtn');
    const emailForm = document.getElementById('emailForm');
    const bulkEmailPopup = document.getElementById('bulkEmailPopup');
    const closeBulkEmailPopupBtn = document.getElementById('closeBulkEmailPopupBtn');
    const bulkEmailForm = document.getElementById('bulkEmailForm');
    const scheduleEmailPopup = document.getElementById('scheduleEmailPopup');
    const closeScheduleEmailPopupBtn = document.getElementById('closeScheduleEmailPopupBtn');
    const scheduleEmailForm = document.getElementById('scheduleEmailForm');    
    const attachments = document.getElementById('attachments');

    let maxReceivers = 5;

    // Add more email fields
    addReceiverBtn.addEventListener('click', function () {
        const currentReceivers = receiversList.querySelectorAll('.toEmail').length;
        if (currentReceivers < maxReceivers) {
            const newReceiver = document.createElement('div');
            newReceiver.innerHTML = `
                <input type="email" name="receivers[]" class="toEmail" required>
                <button type="button" class="removeReceiverBtn">Remove</button>
            `;
            receiversList.appendChild(newReceiver);

            newReceiver.querySelector('.removeReceiverBtn').addEventListener('click', function () {
                newReceiver.remove();
            });
        } else {
            alert('You can add a maximum of ' + maxReceivers + ' receivers.');
        }
    });

    // Show change email popup
    changeEmailBtn.addEventListener('click', function () {
        emailPopup.classList.remove('hidden');
    });

    // Close the popup
    closePopupBtn.addEventListener('click', function () {
        emailPopup.classList.add('hidden');
    });

    // Show bulk email popup
    bulkEmailBtn.addEventListener('click', function () {
        bulkEmailPopup.classList.remove('hidden');
    });

    // Close bulk email popup
    closeBulkEmailPopupBtn.addEventListener('click', function () {
        bulkEmailPopup.classList.add('hidden');
    });

    // Handle bulk email form submission
    bulkEmailForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const numEmails = document.getElementById('numEmails').value;
        const interval = document.getElementById('interval').value;
        const fromEmail = document.getElementById('fromEmail').value;
        const password = document.getElementById('emailPassword').value;
        const receivers = Array.from(document.querySelectorAll('.toEmail')).map(input => input.value);
        const subject = document.getElementById('subject').value;
        const body = document.getElementById('body').value;

        const formData = new FormData();
        formData.append('numEmails', numEmails);
        formData.append('interval', interval);
        formData.append('sender', fromEmail);
        formData.append('password', password);
        formData.append('subject', subject);
        formData.append('body', body);
        formData.append('receivers', JSON.stringify(receivers));

        // Handle attachments
        for (let i = 0; i < attachments.files.length; i++) {
            formData.append('attachments', attachments.files[i]);  // Append each file properly
        }

        // Send bulk email request
        fetch('/send_bulk_email', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });

        bulkEmailPopup.classList.add('hidden');
    });

    // Show schedule email popup
    scheduleEmailBtn.addEventListener('click', function () {
        scheduleEmailPopup.classList.remove('hidden');
    });

    // Close schedule email popup
    closeScheduleEmailPopupBtn.addEventListener('click', function () {
        scheduleEmailPopup.classList.add('hidden');
    });

    // Handle schedule email form submission
    scheduleEmailForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const scheduleTime = document.getElementById('scheduleTime').value;
        const fromEmail = document.getElementById('fromEmail').value;
        const password = document.getElementById('emailPassword').value;
        const receivers = Array.from(document.querySelectorAll('.toEmail')).map(input => input.value);
        const subject = document.getElementById('subject').value;
        const body = document.getElementById('body').value;

        const formData = new FormData();

        formData.append('scheduleTime', scheduleTime);
        formData.append('sender', fromEmail);
        formData.append('password', password);
        formData.append('subject', subject);
        formData.append('receivers', JSON.stringify(receivers));
        formData.append('body', body);

        // Handle attachments
        for (let i = 0; i < attachments.files.length; i++) {
            formData.append('attachments', attachments.files[i]);  // Append each file properly
        }

        // Send schedule email request
        fetch('/schedule_email', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });

        scheduleEmailPopup.classList.add('hidden');
    });

    // Handle changing the sender email
    changeEmailForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const newEmail = document.getElementById('newEmail').value;
        fromEmail.value = newEmail;
        emailPopup.classList.add('hidden');
    });

    // Handle email form submission
    emailForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Retrieve form values at the time of form submission
        const fromEmail = document.getElementById('fromEmail').value;
        const password = document.getElementById('emailPassword').value;
        const receivers = Array.from(document.querySelectorAll('.toEmail')).map(input => input.value);
        const subject = document.getElementById('subject').value;
        const body = document.getElementById('body').value;

        const formData = new FormData();
        formData.append('sender', fromEmail);
        formData.append('password', password);
        formData.append('subject', subject);
        formData.append('body', body);
        formData.append('receivers', JSON.stringify(receivers));

        // Handle attachments
        for (let i = 0; i < attachments.files.length; i++) {
            formData.append('attachments', attachments.files[i]);  // Append each file properly
        }

        console.log([...formData.entries()]); // Check the contents of formData

        fetch('/send_mail', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
