# from WebInterface.utils import getContext
# from WebInterface.modules.competition.context import SummaryCompetitionContext
# from WebInterface.modules.competition.context import ListCompetitionContext
# from WebInterface.modules.competition.context import CreateCompetitionContext

# templatePathPrefix = "competition/templates/management/"

# # def summary(request, organizationUrl):
# # 	pageTemplate = templatePathPrefix + "summary.html"
# # 	return getContext(SummaryCompetitionContext, pageTemplate, request, organizationUrl = organizationUrl)

# def listCompetitions(request, organizationUrl):
# 	pageTemplate = templatePathPrefix + "summary.html"
# 	return getContext(ListCompetitionContext, request, page_template = pageTemplate, organizationUrl = organizationUrl)

# def createCompetition(request, organizationUrl):
# 	pageTemplate = templatePathPrefix + "createCompetition.html"
# 	return getContext(CreateCompetitionContext, request, page_template = pageTemplate, organizationUrl = organizationUrl)