/* eslint-disable no-underscore-dangle */
class API {
  /**
   * get and cache config object
   * @return object
   */
  static getConfig() {
    if (API.configCache == null) {
      API.configCache = $.get("serve_config.json");
    }
    return API.configCache;
  }

  static getCalendar() {
    return $.get("serve_main_calendar.json");
  }

  static getPapers() {
    if (API.paperCache == null) {
      API.paperCache = $.get("papers.json");
    }
    return API.paperCache;
  }

  static getPapersAndProjection() {
    return Promise.all([
      API.getPapers(),
      $.get("serve_papers_projection.json"),
    ]);
  }

  /**
   * lazy store creation/loading - not needed if own store backend
   * @see API.storeIDs
   * @return object
   */
  static getStore(storeID) {
    if (!(storeID in API._storeCaches)) {
      API._storeCaches[storeID] = new Persistor(
        `miniconf-${API.getConfig().name}-${storeID}`
      );
    }
    return API._storeCaches[storeID];
  }

  /**
   * get marks for all papers of a specific type
   * @see API.storeIDs
   * @param storeID
   * @return {Promise<object>}
   */
  static async markGetAll(storeID) {
    return API.getStore(storeID).getAll();
  }

  static async markSet(storeID, paperID, read = true) {
    return API.getStore(storeID).set(paperID, read);
  }

  /*
   * Resource paths
   */

  /**
   * Link to thumbnails derived from paper object
   * @param paper
   * @return {string}
   */
  static thumbnailPath(paper) {
    // paper.pic_id contains a google drive url as follows: https://drive.google.com/file/d/1bDKJUha7CfprIh1jVxLcMZ1aUzb7_kJK/view?usp=drive_link. We need whatever comes after /d/
    const id = paper.pic_id.split("/")[5];
    return `https://drive.google.com/thumbnail?id=${id}`;
    // return `https://drive.google.com/thumbnail?id=1bDKJUha7CfprIh1jVxLcMZ1aUzb7_kJK`;
  }

  /**
   * Link to poster detail derived from paper object
   * @param paper
   * @return {string}
   */
  static posterLink(paper) {
    return `poster_${paper.id}.html`;
  }

  /**
   * link to the poster ICAL file for poster and repetition i
   * @param paper
   * @param i
   * @return {string}
   */
  static posterICS(paper, i) {
    return `webcal://iclr.github.io/iclr-images/calendars/poster_${paper.UID}.${i}.ics`;
  }
}

API.configCache = null;
API.paperCache = null;
API._storeCaches = {};
API.storeIDs = {
  visited: "visited",
  bookmarked: "bookmark",
};
