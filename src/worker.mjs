export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.hostname === "www.wuwabanners.net") {
      url.hostname = "wuwabanners.net";
      return Response.redirect(url.toString(), 308);
    }

    return env.ASSETS.fetch(request);
  },
};
