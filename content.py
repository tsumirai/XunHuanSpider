class Content:
    def Simple(self, jump_url, title):
        dict = {}
        dict['title'] = title
        dict['jump_url'] = jump_url
        return dict

    def Complete(self, title, content, imageUrls, qq, wx, tid, url):
        dict = {}
        dict['title'] = title
        dict['content'] = content
        dict['image_urls'] = imageUrls
        dict['qq'] = qq
        dict['wx'] = wx
        dict['tid'] = tid
        dict['url'] = url
        return dict
