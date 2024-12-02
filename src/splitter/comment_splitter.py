# %%
import re

class CommentSplitter:

    def __init__(self) -> None:
        self.expressions = ["happy", "sad", "cry", "surprise", "angry", "neutral"]

    def expressions_splitter(self,text) -> list:
        matches = re.findall(r"\[(.*?)\](.*?)(?=\[|$)",text)
        result = [{"Expression": match[0], "Text": match[1].strip()} for match in matches]
        result = self._fix(result)
        return result
    
    def expressions_remover(self,dictlist) -> str:
        result = []
        for item in dictlist:
            comment = item["Text"]
            result.append(comment)
        result = " ".join(result)
        return result
    
    def _fix(self,dictlist) -> list:
        result = []
        for item in dictlist:
            if item["Expression"] not in self.expressions:
                item["Expression"] = "neutral"
            result.append(item)
        return result

if __name__ == "__main__":
    text = "[happy]今日はいい天気だね！[s0d]でも午後から雨が降るらしい...[cry]今日はディズニーにいくのに"
    cs = CommentSplitter()
    result = cs.expressions_splitter(text)
    print(result)
    text = cs.expressions_remover(result)
    print(text)
# %%
