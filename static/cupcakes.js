class Cupcake {
  constructor() {
    // Initializes properties using jQuery selectors.
    this.$cupcakeList = $(".list-group");
    this.$searchForm = $("#search-form");

    // Calls `addEventListeners` to bind event handlers
    this.addEventListeners();
  }

  // *** STATIC METHODS (not called on instances) ***

  // get all cupcakes
  static async fetchAllCupcakes() {
    try {
      // fetches all cupcakes data from the server using axios API call
      const resp = await axios.get("/api/cupcakes");
      // return an array of cupcakes
      return resp.data.cupcakes;
    } catch (err) {
      console.error("Fetch error: ", err);
    }
  }

  // add cupcake
  static async createCupcake(data) {
    try {
      // Takes cupcake data as an object
      // Sends a POST request to the server to create a new cupcake
      const resp = await axios.post("/api/cupcakes", data);
      // Return the newly created cupcake data.
      return resp.data.cupcake;
    } catch (err) {
      console.error("Error creating cupcakes: ", err);
    }
  }

  // search cupcake
  static async searchCupcake(searchTerm) {
    try {
      // Takes a search term and sends a GET request to the server
      // with the search term as parameter
      const resp = await axios.get("/api/cupcakes/search", {
        params: {
          term: searchTerm,
        },
      });
      // Returns the filtered cupcakes data.
      return resp.data.cupcakes;
    } catch (err) {
      console.error("Error: ", err);
    }
  }

  // *** INSTANCE METHODS ***

  // updating cupcake
  async updateCupcake(id, data) {
    try {
      // Sends a PATCH request to update a cupcake
      // `await` pauses the function execution until the request is completed and the response is received.
      const resp = await axios.patch(`/api/cupcakes/${id}`, data);
      console.log(resp.data);
      return resp.data.cupcake;
    } catch (err) {
      console.log("Error updating cupcake: ", err);
    }
  }

  // delete cupcake
  // Asynchronous function takes an `id` argument
  async deleteCupcake(id) {
    try {
      // Sends a DELETE request to the server to remove a cupcake
      // `await` pauses the function execution until the request is completed and the response is received
      const resp = await axios.delete(`/api/cupcakes/${id}`);
      console.log(resp.data);

      return resp.data;
    } catch (err) {
      console.error("Error deleting cupcake: ", err);
    }
  }

  // Takes an array of cupcakes and updates the HTML to display them.
  dispalyCupcakes(cupcakes) {
    // Clear existing list
    $(".list-group").empty();

    // Loop through cupcakes
    for (let cupcake of cupcakes) {
      // Generate HTML for each cupcake
      const newLi = this.makeLiHTML(cupcake);

      // Append HTML to the list
      $(".list-group").append(newLi);
    }
  }

  // Creates an HTML for a single cupcake list item
  makeLiHTML(cupcake) {
    return `<li class="list-group-item d-flex justify-content-between align-items-center" data-id="${cupcake.id}">${cupcake.flavor}
        <a href="/edit-cupcake/${cupcake.id}" class="btn btn-primary btn-sm">Update</a>
        <button class="btn btn-danger btn-sm delete-btn">Delete</button>
        </li>`;
  }

  addEventListeners() {
    // Add cupcake
    // Using an arrow function to preserve the context ('this'),
    // ensure that 'this` refers to the `Cupcake` instance,
    // Allowing me to access its properties correctly such as `$cupcakeList`
    $(".add-cupcake").on("submit", async (e) => {
      e.preventDefault();

      const $flavor = $("#flavor").val();
      const $size = $("#size").val();
      const $rating = parseFloat($("#rating").val()); // string converted to float
      const $image = $("#image").val();
      const $csrfToken = $("#csrf_token").val();

      const formData = {
        flavor: $flavor,
        size: $size,
        rating: $rating,
        image: $image,
        csrf_token: $csrfToken,
      };

      try {
        const newCupcake = await Cupcake.createCupcake(formData);
        console.log(newCupcake);

        if (newCupcake) {
          // Update the UI with the new cupcake.
          const newLi = this.makeLiHTML(newCupcake);
          this.$cupcakeList.append(newLi);
        } else {
          console.error("Error creating cupcake: No cupcake data returned.");
        }
      } catch (err) {
        console.error("Error creating cupcake: ", error);
      }

      $("#flavor").val("");
      $("#size").val("");
      $("#rating").val("");
      $("#image").val("");
    });

    // Search cupcake
    $("#search-btn").on("click", async (e) => {
      e.preventDefault();

      const $searchTerm = $("#search-term").val();
      const cupcakes = await Cupcake.searchCupcake($searchTerm);

      this.dispalyCupcakes(cupcakes);
    });

    // Deteleting cupcake
    // Event delegation for handling dynamically created delete buttons
    this.$cupcakeList.on("click", ".delete-btn", async (e) => {
      e.preventDefault();

      const $cupcake = $(e.target).closest("li");
      const id = $cupcake.data("id");
      const deletedCupcake = await this.deleteCupcake(id);
      if (deletedCupcake) {
        $cupcake.remove();
      }
    });

    // Update cupcake event listener
    $("#save-update").on("submit", async (e) => {
      e.preventDefault();
      // Get the cupcake ID (assuming it's stored somewhere or passed to this form)

      // Extract the cupcake ID
      const id = $("#cupcake-id").val();

      // Gather updated data from the form fields
      const $flavor = $("#flavor").val();
      const $size = $("#size").val();
      const $rating = parseFloat($("#rating").val());
      const $image = $("#image").val();
      const $csrfToken = $("#csrf_token").val();

      const formData = {
        flavor: $flavor,
        size: $size,
        rating: $rating,
        image: $image,
        csrf_token: $csrfToken,
      };

      // Call updateCupcake method
      await this.updateCupcake(id, formData);
    });
  }
}

$(document).ready(async () => {
  const app = new Cupcake();
  const cupcakes = await Cupcake.fetchAllCupcakes();
  app.dispalyCupcakes(cupcakes);
});
