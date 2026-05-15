document.addEventListener("DOMContentLoaded", function () {
    setupRegistrationSearch();
    setupModalOutsideClick();
    setupEscapeToClose();
});

function setupRegistrationSearch() {
    const searchInput = document.getElementById("searchInput");
    const table = document.getElementById("registrationTable");
    const visibleCountText = document.getElementById("visibleCountText");

    if (!searchInput || !table) {
        return;
    }

    const tbodyRows = table.querySelectorAll("tbody tr");

    function updateVisibleCount() {
        let visibleRows = 0;

        tbodyRows.forEach(function (row) {
            if (row.style.display !== "none" && !row.querySelector(".empty-cell")) {
                visibleRows++;
            }
        });

        if (visibleCountText) {
            visibleCountText.textContent = "Visible registrations: " + visibleRows;
        }
    }

    searchInput.addEventListener("keyup", function () {
        const filterValue = searchInput.value.toLowerCase();

        tbodyRows.forEach(function (row) {
            if (row.querySelector(".empty-cell")) {
                return;
            }

            const rowText = row.innerText.toLowerCase();
            row.style.display = rowText.includes(filterValue) ? "" : "none";
        });

        updateVisibleCount();
    });

    updateVisibleCount();
}

function openRegisterModalFromCard(cardElement) {
    const eventName = cardElement.dataset.eventName || "";
    const eventDescription = cardElement.dataset.eventDescription || "";
    const eventDate = cardElement.dataset.eventDate || "";

    document.getElementById("selectedEventTitle").textContent = eventName;
    document.getElementById("selectedEventDescription").textContent = eventDescription;
    document.getElementById("selectedEventDate").textContent = eventDate;
    document.getElementById("selectedEventInput").value = eventName;

    openModal("registerModal");
}

function openRegisterModalUsingKeyboard(event, cardElement) {
    if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openRegisterModalFromCard(cardElement);
    }
}

function closeRegisterModal() {
    closeModal("registerModal");
}

function openAddModal() {
    openModal("addEventModal");
}

function closeAddModal() {
    closeModal("addEventModal");
}

function openEditModalFromButton(buttonElement) {
    const eventId = buttonElement.dataset.eventId || "";
    const eventName = buttonElement.dataset.eventName || "";
    const eventDescription = buttonElement.dataset.eventDescription || "";
    const eventDate = buttonElement.dataset.eventDate || "";

    document.getElementById("editEventForm").action = "/edit-event/" + eventId;
    document.getElementById("editEventName").value = eventName;
    document.getElementById("editEventDescription").value = eventDescription;
    document.getElementById("editEventDate").value = eventDate;

    openModal("editEventModal");
}

function closeEditModal() {
    closeModal("editEventModal");
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);

    if (modal) {
        modal.classList.add("show");
        document.body.style.overflow = "hidden";
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);

    if (modal) {
        modal.classList.remove("show");
    }

    const openModalCount = document.querySelectorAll(".modal.show").length;
    if (openModalCount === 0) {
        document.body.style.overflow = "";
    }
}

function setupModalOutsideClick() {
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("modal")) {
            event.target.classList.remove("show");
            document.body.style.overflow = "";
        }
    });
}

function setupEscapeToClose() {
    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") {
            return;
        }

        const visibleModals = document.querySelectorAll(".modal.show");
        visibleModals.forEach(function (modal) {
            modal.classList.remove("show");
        });

        document.body.style.overflow = "";
    });
}
