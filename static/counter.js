window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://127.0.0.1:8480/ws");

  document.querySelector(".minus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "minus" }));
  });
  document.querySelector(".plus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "plus" }));
  });
  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "value":
        document.querySelector(".value").textContent = event.value;
        break;
      case "users":
        const users = `${event.count} user${event.count == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        break;
      case "data":
            const el = document.createElement('div');
            el.classList.add('dataClass');
            el.textContent = event.value;
            let cons = document.querySelector(".console");
            cons.insertBefore(el, cons.firstChild);
            //document.querySelector(".console").insertAdjacentHTML('beforebegin', el);
            break;
      default:
        console.error("unsupported event", event);
    }
  };
});