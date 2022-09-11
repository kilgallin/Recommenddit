import praw

user_agent = "Get top 1000 post in each subreddit / Suphanut & JD"

r = praw.Reddit(user_agent=user_agent)

def searchtop(header):
    post_count = 0
    # edit limit to 100 if you want to
    submissions = r.get_subreddit(header).get_top_from_all(limit=1000)
    for post in submissions:
                if not post.author:
                    name = '[deleted]'
                else:
                    name = post.author.name
                print name, " ", post.subreddit, " score: ", post.score
                post_count+=1
    print "getting total: ", post_count, " post"
            


def main():
	r = praw.Reddit(user_agent = user_agent)
    # edit your redditlist file 
	with open('redditlist.txt') as f:
            subreddit_list = f.readlines()
            #count = 0
            for x in subreddit_list:
                    subreddit_name = x.split()
                    header = subreddit_name[0]
                    print "Start searching top 1000 post in /r/", header
                    searchtop(header)

if __name__ == '__main__':
	main()