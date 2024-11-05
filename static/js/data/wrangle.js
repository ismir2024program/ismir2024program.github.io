const calcAllKeys = function (allPapers, allKeys) {
  console.log(allPapers);
  const collectAuthors = new Set();
  const collectKeywords = new Set();
  const collectSessions = new Set();


  allPapers.forEach((d) => {
    console.log(d);
    d.content.authors.forEach((a) => collectAuthors.add(a));
    d.content.keywords.forEach((a) => collectKeywords.add(a));
    d.content.session.forEach((a) => collectSessions.add(a));
    allKeys.titles.push(d.title);
  });
  allKeys.authors = Array.from(collectAuthors);
  allKeys.keywords = Array.from(collectKeywords);
  allKeys.sessions = Array.from(collectSessions);
  allKeys.sessions.sort();
  console.log(allKeys.keywords)
};
