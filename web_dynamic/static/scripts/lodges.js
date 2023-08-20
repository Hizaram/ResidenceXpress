document.ready(function () {
	const HOST = "http://127.0.0.1:5001";
	const amenities = {};
	const cities = {};
	const states = {};

// fetch data about lodges
	$.post({
		url: `${HOST}/api/v1/lodges_search`,
		data: JSON.stringify({}),
		headers: {
			"Content-Type": "application/json",
		},
		success: (data) => {
			data.forEach((lodge) =>
				$("section.property").append(
					`<div class="container">

          <p class="section-subtitle">Properties</p>

          <h2 class="h2 section-title">Featured Listings</h2>

          <ul class="property-list has-scrollbar">
            <li>
		    <div class="property-card" data-id="${ lodge.id }">

                <figure class="card-banner">

			<a href="/view_lodge/${ lodge.id }">
                    <img src="../static/images/property-1.jpg" alt="New Apartment Nice View" class="w-100">
                  </a>

                  <div class="card-badge green">For Rent</div>

                  <div class="banner-actions">

                    <button class="banner-actions-btn">
                      <ion-icon name="location"></ion-icon>

		      <address>${lodge.streets.name}, ${lodge.streets.location.name}</address>
                    </button>

                    <button class="banner-actions-btn">
                      <ion-icon name="camera"></ion-icon>

                      <span>4</span>
                    </button>

                    <button class="banner-actions-btn">
                      <ion-icon name="film"></ion-icon>

                      <span>2</span>
                    </button>

                  </div>

                </figure>

                <div class="card-content">

                  <div class="card-price">
			  <strong>${ lodge.price }</strong>/Month
                  </div>

                  <h3 class="h3 card-title">
			  <a href="/view_lodge/${ lodge.id }">${ lodge.name }</a>
                  </h3>

                  <p class="card-text">
		  ${ lodge.description }
                  </p>

                  <ul class="card-list">

                    <li class="card-item">
			    <strong>${ lodge.number_rooms }</strong>

                      <ion-icon name="bed-outline"></ion-icon>

                      <span>Bedrooms</span>
                    </li>

                    <li class="card-item">
                      <strong>2</strong>

                      <ion-icon name="man-outline"></ion-icon>

                      <span>Bathrooms</span>
                    </li>

                    <li class="card-item">
                      <strong>3450</strong>

                      <ion-icon name="square-outline"></ion-icon>

                      <span>Square Ft</span>
                    </li>

                  </ul>

                </div>

                <div class="card-footer">

                  <div class="card-author">

                    <figure class="author-avatar">
                      <img src="../static/images/author.jpg" alt="William Seklo" class="w-100">
                    </figure>

                    <div>
                      <p class="author-name">
		      <a href="/view_user_details/${ lodge.user.id }">${ lodge.user.first_name }, ${ lodge.user.last_name }</a>
                      </p>

                      <p class="author-title">Caretaker</p>
                    </div>

                  </div>

                  <div class="card-footer-actions">

                    <button class="card-footer-actions-btn">
                      <ion-icon name="resize-outline"></ion-icon>
                    </button>

                    <button class="card-footer-actions-btn">
                      <ion-icon name="heart-outline"></ion-icon>
                    </button>

                    <button class="card-footer-actions-btn">
                      <ion-icon name="add-circle-outline"></ion-icon>
                    </button>

                  </div>

                </div>

              </div>
            </li>
          </ul>
        </div>`
				)
			);
		},
		dataType: "json";
	});
});
