const BASE_URL = "http://127.0.0.1:5000";

export async function predictText(text) {
  const response = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({text: text,
    user_id: localStorage.getItem("userId") }),
  });

  return response.json();
}
export const getPredictionHistory = async () => {
  const user_id = localStorage.getItem("userId");

  const res = await fetch(
    `http://localhost:5000/user/predictions/${user_id}`
  );

  return res.json();
};



export async function predictImage(file) {
  const formData = new FormData();
  formData.append("image", file);
  formData.append("user_id", localStorage.getItem("userId"));

  const response = await fetch(`${BASE_URL}/predict-image`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}
