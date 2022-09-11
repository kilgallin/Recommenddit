def search(self, query, subreddit=None, sort=None, syntax=None,
               period=None, timestamps=[], *args, **kwargs):
        """Return a generator for submissions that match the search query.

        :param query: The query string to search for. If query is a URL only
            submissions which link to that URL will be returned.
        :param subreddit: Limit search results to the subreddit if provided.
        :param sort: The sort order of the results.
        :param syntax: The syntax of the search query.
        :param period: The time period of the results.

        The additional parameters are passed directly into
        :meth:`.get_content`. Note: the `url` and `param` parameters cannot be
        altered.

        See http://www.reddit.com/help/search for more information on how to
        build a search query.

        """

        params = {}
        if sort:
            params['sort'] = sort
        if syntax:
            params['syntax'] = syntax
        if period:
            params['t'] = period
        if len(timestamps) == 2:
            params['syntax'] = "cloudsearch"
            timestamps = "timestamp:%d..%d" % (timestamps[0], timestamps[1])
            if len(query) > 0:
                query = "(and %s (and %s))" % (query, timestamps)
            else:
                query = timestamps
        params['q'] = query
        if subreddit:
            params['restrict_sr'] = 'on'
            url = self.config['search'] % subreddit
        else:
            url = self.config['search'] % 'all'

        depth = 2
        while depth > 0:
            depth -= 1
            try:
                for item in self.get_content(url, params=params, *args,
                                             **kwargs):
                    yield item
                break
            except errors.RedirectException as exc:
                parsed = urlparse(exc.response_url)
                params = dict((k, ",".join(v)) for k, v in
                              parse_qs(parsed.query).items())
                url = urlunparse(parsed[:3] + ("", "", ""))
                # Handle redirects from URL searches
                if 'already_submitted' in params:
                    yield self.get_submission(url)
                    break