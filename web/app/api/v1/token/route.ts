const BACKEND_URL = "http://localhost:8000";
export const POST = async (request: Request) => {
  const body = await request.json();
  const response = await fetch(BACKEND_URL + "/api/v1/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  const result = await response.json();
  return new Response(JSON.stringify(result), { status: response.status });
};
