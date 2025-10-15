import type { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core'
export type Maybe<T> = T | null
export type InputMaybe<T> = T | null | undefined
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> }
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> }
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = {
	[_ in K]?: never
}
export type Incremental<T> =
	| T
	| { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never }
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
	ID: { input: string; output: string }
	String: { input: string; output: string }
	Boolean: { input: boolean; output: boolean }
	Int: { input: number; output: number }
	Float: { input: number; output: number }
	/** Date with time (isoformat) */
	DateTime: { input: Date; output: Date }
	/** BigInt field */
	Union: { input: number; output: number }
}

export type BulkTaskResult = {
	__typename?: 'BulkTaskResult'
	failure: Scalars['Int']['output']
	success: Scalars['Int']['output']
	total: Scalars['Int']['output']
}

export type Mutation = {
	__typename?: 'Mutation'
	/** Add Wikibase */
	addWikibase: Wikibase
	/** Add Language to Wikibase */
	addWikibaseLanguage: Scalars['Boolean']['output']
	/** Fetch Connectivity Data from Specified Wikibase Instance */
	fetchConnectivityData: Scalars['Boolean']['output']
	/** Fetch External Identifier Data from Specified Wikibase Instance */
	fetchExternalIdentifierData: Scalars['Boolean']['output']
	/** Fetch Log Data from Specified Wikibase Instance */
	fetchLogData: Scalars['Boolean']['output']
	/** Fetch Property Popularity from Specified Wikibase Instance */
	fetchPropertyPopularityData: Scalars['Boolean']['output']
	/** Fetch Quantity Data from Specified Wikibase Instance */
	fetchQuantityData: Scalars['Boolean']['output']
	/** Fetch Recent Changes Data from Specified Wikibase Instance */
	fetchRecentChangesData: Scalars['Boolean']['output']
	/** Fetch Special:Statistics Data */
	fetchStatisticsData: Scalars['Boolean']['output']
	/** Fetch Time to First Value Data from Specified Wikibase Instance */
	fetchTimeToFirstValueData: Scalars['Boolean']['output']
	/** Fetch User Data from Specified Wikibase Instance */
	fetchUserData: Scalars['Boolean']['output']
	/** Scrape data from Special:Version page */
	fetchVersionData: Scalars['Boolean']['output']
	/** Merge Software */
	mergeSoftwareById: Scalars['Boolean']['output']
	/** Remove Language from Wikibase */
	removeWikibaseLanguage: Scalars['Boolean']['output']
	/** Remove URL from Wikibase */
	removeWikibaseUrl: Scalars['Boolean']['output']
	/** Set Extension Bundled with WBS */
	setExtensionWbsBundled: Scalars['Boolean']['output']
	/** Fetch Connectivity Data from All Wikibase Instances */
	updateAllConnectivityData: BulkTaskResult
	/** Fetch External Identifier Data from All Wikibase Instances */
	updateAllExternalIdentifierData: BulkTaskResult
	/** Fetch Log Data from All Wikibase Instances */
	updateAllLogData: BulkTaskResult
	/** Fetch Property Popularity from All Wikibase Instances */
	updateAllPropertyPopularityData: BulkTaskResult
	/** Fetch Quantity Data from All Wikibase Instances */
	updateAllQuantityData: BulkTaskResult
	/** Fetch Recent Changes Data from All Wikibase Instances */
	updateAllRecentChangesData: BulkTaskResult
	/** Fetch Special:Statistics Data for All Wikibase Instances */
	updateAllStatisticsData: BulkTaskResult
	/** Fetch Time to First Value Data from All Wikibase Instances */
	updateAllTimeToFirstValueData: BulkTaskResult
	/** Fetch User Data from All Wikibase Instances */
	updateAllUserData: BulkTaskResult
	/** Scrape data from Special:Version page for All Wikibase Instances */
	updateAllVersionData: BulkTaskResult
	/** Update the list of known Wikibase Cloud instances from API */
	updateCloudInstances: Scalars['Boolean']['output']
	/** Update Wikibase Primary Language */
	updateWikibasePrimaryLanguage: Scalars['Boolean']['output']
	/** Update Wikibase Type */
	updateWikibaseType: Scalars['Boolean']['output']
	/** Add / Update Wikibase URL */
	upsertWikibaseUrl: Scalars['Boolean']['output']
}

export type MutationAddWikibaseArgs = {
	wikibaseInput: WikibaseInput
}

export type MutationAddWikibaseLanguageArgs = {
	language: Scalars['String']['input']
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchConnectivityDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchExternalIdentifierDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchLogDataArgs = {
	firstMonth: Scalars['Boolean']['input']
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchPropertyPopularityDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchQuantityDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchRecentChangesDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchStatisticsDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchTimeToFirstValueDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchUserDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationFetchVersionDataArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type MutationMergeSoftwareByIdArgs = {
	additionalId: Scalars['Int']['input']
	baseId: Scalars['Int']['input']
}

export type MutationRemoveWikibaseLanguageArgs = {
	language: Scalars['String']['input']
	wikibaseId: Scalars['Int']['input']
}

export type MutationRemoveWikibaseUrlArgs = {
	urlType: WikibaseUrlType
	wikibaseId: Scalars['Int']['input']
}

export type MutationSetExtensionWbsBundledArgs = {
	bundled?: Scalars['Boolean']['input']
	extensionId: Scalars['Int']['input']
}

export type MutationUpdateAllLogDataArgs = {
	firstMonth: Scalars['Boolean']['input']
}

export type MutationUpdateWikibasePrimaryLanguageArgs = {
	language: Scalars['String']['input']
	wikibaseId: Scalars['Int']['input']
}

export type MutationUpdateWikibaseTypeArgs = {
	wikibaseId: Scalars['Int']['input']
	wikibaseType?: InputMaybe<WikibaseType>
}

export type MutationUpsertWikibaseUrlArgs = {
	url: Scalars['String']['input']
	urlType: WikibaseUrlType
	wikibaseId: Scalars['Int']['input']
}

export type PageMetadata = {
	__typename?: 'PageMetadata'
	/** Page Number - 1-indexed - input */
	pageNumber: Scalars['Union']['output']
	/** Page Size - input */
	pageSize: Scalars['Union']['output']
	/** Total Number of Records */
	totalCount: Scalars['Union']['output']
	/** Total Number of Pages */
	totalPages: Scalars['Union']['output']
}

export type Query = {
	__typename?: 'Query'
	/** Aggregated Year of First Log Date */
	aggregateCreated: Array<WikibaseYearCreatedAggregate>
	/** Aggregated Extension Popularity */
	aggregateExtensionPopularity: WikibaseSoftwareVersionDoubleAggregatePage
	/** Aggregated External Identifier */
	aggregateExternalIdentifier: WikibaseExternalIdentifierAggregate
	/** Aggregated Language Popularity */
	aggregateLanguagePopularity: WikibaseLanguageAggregatePage
	/** Aggregated Library Popularity */
	aggregateLibraryPopularity: WikibaseSoftwareVersionDoubleAggregatePage
	/** Aggregated Property Popularity */
	aggregatePropertyPopularity: WikibasePropertyPopularityAggregateCountPage
	/** Aggregated Quantity */
	aggregateQuantity: WikibaseQuantityAggregate
	/** Aggregated Recent Changes */
	aggregateRecentChanges: WikibaseRecentChangesAggregate
	/** Aggregated Skin Popularity */
	aggregateSkinPopularity: WikibaseSoftwareVersionDoubleAggregatePage
	/** Aggregated Software Popularity */
	aggregateSoftwarePopularity: WikibaseSoftwareVersionDoubleAggregatePage
	/** Aggregated Statistics */
	aggregateStatistics: WikibaseStatisticsAggregate
	/** Aggregated Users */
	aggregateUsers: WikibaseUserAggregate
	/** List of Extensions */
	extensionList: WikibaseSoftwarePage
	/** Wikibase Instance */
	wikibase: Wikibase
	/** List of Wikibases */
	wikibaseList: WikibasePage
}

export type QueryAggregateCreatedArgs = {
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateExtensionPopularityArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateExternalIdentifierArgs = {
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateLanguagePopularityArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateLibraryPopularityArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregatePropertyPopularityArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateQuantityArgs = {
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateRecentChangesArgs = {
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateSkinPopularityArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateSoftwarePopularityArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateStatisticsArgs = {
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryAggregateUsersArgs = {
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type QueryExtensionListArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
}

export type QueryWikibaseArgs = {
	wikibaseId: Scalars['Int']['input']
}

export type QueryWikibaseListArgs = {
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}

export type Wikibase = {
	__typename?: 'Wikibase'
	/** Wikibase Category */
	category?: Maybe<WikibaseCategory>
	/** Connectivity Data */
	connectivityObservations: WikibaseConnectivityObservationWikibaseObservationSet
	/** Description */
	description?: Maybe<Scalars['String']['output']>
	/** External Identifier Data */
	externalIdentifierObservations: WikibaseExternalIdentifierObservationWikibaseObservationSet
	id: Scalars['ID']['output']
	/** Languages */
	languages: WikibaseLanguageSet
	/** Wikibase Location */
	location: WikibaseLocation
	/** Log Data */
	logObservations: WikibaseLogObservation
	/** Organization */
	organization?: Maybe<Scalars['String']['output']>
	/** Property Popularity Data */
	propertyPopularityObservations: WikibasePropertyPopularityObservationWikibaseObservationSet
	/** Quantity Data */
	quantityObservations: WikibaseQuantityObservationWikibaseObservationSet
	/** Recent Changes Data */
	recentChangesObservations: WikibaseRecentChangesObservationWikibaseObservationSet
	/** Software Version Data */
	softwareVersionObservations: WikibaseSoftwareVersionObservationWikibaseObservationSet
	/** Statistics Data */
	statisticsObservations: WikibaseStatisticsObservationWikibaseObservationSet
	/** Time to First Value Data */
	timeToFirstValueObservations: WikibaseTimeToFirstValueObservationWikibaseObservationSet
	/** Wikibase Name */
	title: Scalars['String']['output']
	/** URLs */
	urls: WikibaseUrlSet
	/** User Data */
	userObservations: WikibaseUserObservationWikibaseObservationSet
	/** Cloud, Suite, Other */
	wikibaseType?: Maybe<WikibaseType>
}

export enum WikibaseCategory {
	CulturalAndHistorical = 'CULTURAL_AND_HISTORICAL',
	DigitalCollectionsAndArchives = 'DIGITAL_COLLECTIONS_AND_ARCHIVES',
	EducationalAndReferenceCollections = 'EDUCATIONAL_AND_REFERENCE_COLLECTIONS',
	ExperimentalAndPrototypeProjects = 'EXPERIMENTAL_AND_PROTOTYPE_PROJECTS',
	FictionalAndCreativeWorks = 'FICTIONAL_AND_CREATIVE_WORKS',
	LegalAndPolitical = 'LEGAL_AND_POLITICAL',
	LinguisticAndLiterary = 'LINGUISTIC_AND_LITERARY',
	MathematicsAndScience = 'MATHEMATICS_AND_SCIENCE',
	SemanticAndProsopographicData = 'SEMANTIC_AND_PROSOPOGRAPHIC_DATA',
	SocialAndAdvocacy = 'SOCIAL_AND_ADVOCACY',
	TechnologyAndOpenSource = 'TECHNOLOGY_AND_OPEN_SOURCE'
}

export type WikibaseConnectivityObservation = {
	__typename?: 'WikibaseConnectivityObservation'
	/** Average Distance of Connected Items */
	averageConnectedDistance?: Maybe<Scalars['Float']['output']>
	/**
	 * Number of Unique Item -> Item Connections (regardless of steps) /
	 *         Number of Items Squared
	 */
	connectivity?: Maybe<Scalars['Float']['output']>
	id: Scalars['ID']['output']
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Number of Items with Number of Relationships */
	relationshipItemCounts: Array<WikibaseConnectivityObservationItemRelationshipCount>
	/** Number of Items with Number of Relationships */
	relationshipObjectCounts: Array<WikibaseConnectivityObservationObjectRelationshipCount>
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
	/** Number of Non-Unique Item -> Item Links Returned */
	returnedLinks?: Maybe<Scalars['Union']['output']>
	/** Number of Unique Item -> Item Connections (direct or indirect) */
	totalConnections?: Maybe<Scalars['Union']['output']>
}

export type WikibaseConnectivityObservationItemRelationshipCount = {
	__typename?: 'WikibaseConnectivityObservationItemRelationshipCount'
	id: Scalars['ID']['output']
	/** Number of Items with This Relationship Count */
	itemCount: Scalars['Union']['output']
	/** Number of Relationships Defined for Item */
	relationshipCount: Scalars['Union']['output']
}

export type WikibaseConnectivityObservationObjectRelationshipCount = {
	__typename?: 'WikibaseConnectivityObservationObjectRelationshipCount'
	id: Scalars['ID']['output']
	/** Number of Object with This Relationship Count */
	objectCount: Scalars['Union']['output']
	/** Number of Relationships Defined for Item */
	relationshipCount: Scalars['Union']['output']
}

export type WikibaseConnectivityObservationWikibaseObservationSet = {
	__typename?: 'WikibaseConnectivityObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseConnectivityObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseConnectivityObservation>
}

export type WikibaseExternalIdentifierAggregate = {
	__typename?: 'WikibaseExternalIdentifierAggregate'
	/** Total External Identifier Properties */
	totalExternalIdentifierProperties: Scalars['Union']['output']
	/** Total External Identifier Statements */
	totalExternalIdentifierStatements: Scalars['Union']['output']
	/** Total URL Properties */
	totalUrlProperties: Scalars['Union']['output']
	/** Total URL Statements */
	totalUrlStatements: Scalars['Union']['output']
	/** Wikibases with External Identifier Data */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseExternalIdentifierObservation = {
	__typename?: 'WikibaseExternalIdentifierObservation'
	id: Scalars['ID']['output']
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
	/** Total External Identifier Properties */
	totalExternalIdentifierProperties?: Maybe<Scalars['Union']['output']>
	/** Total External Identifier Statements */
	totalExternalIdentifierStatements?: Maybe<Scalars['Union']['output']>
	/** Total URL Properties */
	totalUrlProperties?: Maybe<Scalars['Union']['output']>
	/** Total URL Statements */
	totalUrlStatements?: Maybe<Scalars['Union']['output']>
}

export type WikibaseExternalIdentifierObservationWikibaseObservationSet = {
	__typename?: 'WikibaseExternalIdentifierObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseExternalIdentifierObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseExternalIdentifierObservation>
}

export type WikibaseFilterInput = {
	wikibaseType?: InputMaybe<WikibaseTypeInput>
}

export type WikibaseInput = {
	category?: InputMaybe<WikibaseCategory>
	country?: InputMaybe<Scalars['String']['input']>
	description?: InputMaybe<Scalars['String']['input']>
	organization?: InputMaybe<Scalars['String']['input']>
	region?: InputMaybe<Scalars['String']['input']>
	test?: InputMaybe<Scalars['Boolean']['input']>
	urls: WikibaseUrlSetInput
	wikibaseName: Scalars['String']['input']
}

export type WikibaseItemDate = {
	__typename?: 'WikibaseItemDate'
	/** Item Creation Date */
	creationDate: Scalars['DateTime']['output']
	id: Scalars['ID']['output']
	/** Q# for Item */
	q: Scalars['Union']['output']
}

export type WikibaseLanguageAggregate = {
	__typename?: 'WikibaseLanguageAggregate'
	/** Wikibases with this as an additional language */
	additionalWikibases: Scalars['Int']['output']
	/** Language */
	language: Scalars['String']['output']
	/** Wikibases with this as their primary languages */
	primaryWikibases: Scalars['Int']['output']
	/** Wikibases that include this language */
	totalWikibases: Scalars['Int']['output']
}

export type WikibaseLanguageAggregatePage = {
	__typename?: 'WikibaseLanguageAggregatePage'
	/** Data */
	data: Array<WikibaseLanguageAggregate>
	/** Metadata */
	meta: PageMetadata
}

export type WikibaseLanguageSet = {
	__typename?: 'WikibaseLanguageSet'
	/** Additional Languages */
	additional: Array<Scalars['String']['output']>
	/** Primary Language */
	primary?: Maybe<Scalars['String']['output']>
}

export type WikibaseLocation = {
	__typename?: 'WikibaseLocation'
	/** Country */
	country?: Maybe<Scalars['String']['output']>
	/** Region */
	region?: Maybe<Scalars['String']['output']>
}

export type WikibaseLog = {
	__typename?: 'WikibaseLog'
	/** Log Date */
	date: Scalars['DateTime']['output']
}

export type WikibaseLogMonth = {
	__typename?: 'WikibaseLogMonth'
	/** Distinct (Probably) Human User with 5+ Logs Count */
	activeHumanUsers?: Maybe<Scalars['Union']['output']>
	/** Distinct User with 5+ Logs Count */
	activeUsers?: Maybe<Scalars['Union']['output']>
	/** Distinct User Count */
	allUsers?: Maybe<Scalars['Union']['output']>
	/** First Log */
	firstLog?: Maybe<WikibaseLog>
	/** Distinct (Probably) Human User Count */
	humanUsers?: Maybe<Scalars['Union']['output']>
	id: Scalars['ID']['output']
	/** Last Log */
	lastLog?: Maybe<WikibaseLogUser>
	/** Log Count */
	logCount?: Maybe<Scalars['Union']['output']>
	/** Records of Each Type */
	logTypeRecords: Array<WikibaseLogMonthLogType>
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
	/** Records of Each Type */
	userTypeRecords: Array<WikibaseLogMonthUserType>
}

export type WikibaseLogMonthLogType = {
	__typename?: 'WikibaseLogMonthLogType'
	/** Distinct (Probably) Human User with 5+ Logs Count */
	activeHumanUsers?: Maybe<Scalars['Union']['output']>
	/** Distinct User with 5+ Logs Count */
	activeUsers?: Maybe<Scalars['Union']['output']>
	/** Distinct User Count */
	allUsers?: Maybe<Scalars['Union']['output']>
	/** First Log Date */
	firstLogDate: Scalars['DateTime']['output']
	/** Distinct (Probably) Human User Count */
	humanUsers: Scalars['Union']['output']
	id: Scalars['ID']['output']
	/** Last Log Date */
	lastLogDate: Scalars['DateTime']['output']
	/** Log Count */
	logCount?: Maybe<Scalars['Union']['output']>
	/** Log Type */
	logType: WikibaseLogType
}

export type WikibaseLogMonthUserType = {
	__typename?: 'WikibaseLogMonthUserType'
	/** Distinct User with 5+ Logs Count */
	activeUsers?: Maybe<Scalars['Union']['output']>
	/** Distinct User Count */
	allUsers?: Maybe<Scalars['Union']['output']>
	/** First Log Date */
	firstLogDate: Scalars['DateTime']['output']
	id: Scalars['ID']['output']
	/** Last Log Date */
	lastLogDate: Scalars['DateTime']['output']
	/** Log Count */
	logCount?: Maybe<Scalars['Union']['output']>
	/** User Type */
	userType: WikibaseUserType
}

export type WikibaseLogMonthWikibaseObservationSet = {
	__typename?: 'WikibaseLogMonthWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseLogMonth>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseLogMonth>
}

export type WikibaseLogObservation = {
	__typename?: 'WikibaseLogObservation'
	/** First Month's Logs */
	firstMonth: WikibaseLogMonthWikibaseObservationSet
	/** Last Month's Logs */
	lastMonth: WikibaseLogMonthWikibaseObservationSet
}

export enum WikibaseLogType {
	AbuseFilterCreate = 'ABUSE_FILTER_CREATE',
	AbuseFilterModifiy = 'ABUSE_FILTER_MODIFIY',
	AchievementBadge = 'ACHIEVEMENT_BADGE',
	Approve = 'APPROVE',
	CommentsCreate = 'COMMENTS_CREATE',
	CommentsDelete = 'COMMENTS_DELETE',
	ConfigUpdate = 'CONFIG_UPDATE',
	ConsumerApprove = 'CONSUMER_APPROVE',
	ConsumerCreate = 'CONSUMER_CREATE',
	ConsumerDisable = 'CONSUMER_DISABLE',
	ConsumerPropose = 'CONSUMER_PROPOSE',
	ConsumerReject = 'CONSUMER_REJECT',
	ConsumerUpdate = 'CONSUMER_UPDATE',
	ContentModelChange = 'CONTENT_MODEL_CHANGE',
	ContentModelCreate = 'CONTENT_MODEL_CREATE',
	DatadumpDelete = 'DATADUMP_DELETE',
	DatadumpGenerate = 'DATADUMP_GENERATE',
	EventDelete = 'EVENT_DELETE',
	ExportPdf = 'EXPORT_PDF',
	FeedbackCreate = 'FEEDBACK_CREATE',
	FeedbackFeature = 'FEEDBACK_FEATURE',
	FeedbackFlag = 'FEEDBACK_FLAG',
	FeedbackFlagInappropriate = 'FEEDBACK_FLAG_INAPPROPRIATE',
	FeedbackHide = 'FEEDBACK_HIDE',
	FeedbackNoAction = 'FEEDBACK_NO_ACTION',
	FeedbackResolve = 'FEEDBACK_RESOLVE',
	Import = 'IMPORT',
	ImportHtml = 'IMPORT_HTML',
	InterwikiCreate = 'INTERWIKI_CREATE',
	InterwikiDelete = 'INTERWIKI_DELETE',
	InterwikiEdit = 'INTERWIKI_EDIT',
	ItemCreate = 'ITEM_CREATE',
	ItemDelete = 'ITEM_DELETE',
	LockFlowLockTopic = 'LOCK_FLOW_LOCK_TOPIC',
	MediaApprove = 'MEDIA_APPROVE',
	MediaOverwrite = 'MEDIA_OVERWRITE',
	MediaRevert = 'MEDIA_REVERT',
	MediaUpload = 'MEDIA_UPLOAD',
	Move = 'MOVE',
	PageCreate = 'PAGE_CREATE',
	PageDelete = 'PAGE_DELETE',
	PageTranslate = 'PAGE_TRANSLATE',
	PageTranslateDeleteFok = 'PAGE_TRANSLATE_DELETE_FOK',
	PageTranslateDeleteLok = 'PAGE_TRANSLATE_DELETE_LOK',
	PageTranslateMark = 'PAGE_TRANSLATE_MARK',
	PageTranslateReview = 'PAGE_TRANSLATE_REVIEW',
	PageTranslateUnmark = 'PAGE_TRANSLATE_UNMARK',
	PageUpdateLanguage = 'PAGE_UPDATE_LANGUAGE',
	Patrol = 'PATROL',
	PatrolAuto = 'PATROL_AUTO',
	Profile = 'PROFILE',
	PropertyCreate = 'PROPERTY_CREATE',
	PropertyDelete = 'PROPERTY_DELETE',
	Protect = 'PROTECT',
	RedirectDelete = 'REDIRECT_DELETE',
	RedirectMove = 'REDIRECT_MOVE',
	RevisionDelete = 'REVISION_DELETE',
	TableCreate = 'TABLE_CREATE',
	TableDelete = 'TABLE_DELETE',
	TagCreate = 'TAG_CREATE',
	Thank = 'THANK',
	Unapprove = 'UNAPPROVE',
	Unclassified = 'UNCLASSIFIED',
	UndoDelete = 'UNDO_DELETE',
	Unprotect = 'UNPROTECT',
	UserBlock = 'USER_BLOCK',
	UserCreate = 'USER_CREATE',
	UserDelete = 'USER_DELETE',
	UserMerge = 'USER_MERGE',
	UserRename = 'USER_RENAME',
	UserRights = 'USER_RIGHTS',
	UserUnblock = 'USER_UNBLOCK',
	WikiFarm = 'WIKI_FARM',
	WikiGroupDelete = 'WIKI_GROUP_DELETE',
	WikiNamespaces = 'WIKI_NAMESPACES',
	WikiRights = 'WIKI_RIGHTS',
	WikiSettings = 'WIKI_SETTINGS'
}

export type WikibaseLogUser = {
	__typename?: 'WikibaseLogUser'
	/** Log Date */
	date: Scalars['DateTime']['output']
	/** User Type - Bot, User, or Missing? */
	userType?: Maybe<Scalars['String']['output']>
}

export type WikibasePage = {
	__typename?: 'WikibasePage'
	/** Data */
	data: Array<Wikibase>
	/** Metadata */
	meta: PageMetadata
}

export type WikibasePropertyPopularityAggregateCount = {
	__typename?: 'WikibasePropertyPopularityAggregateCount'
	id: Scalars['ID']['output']
	/** Property URL */
	propertyUrl: Scalars['String']['output']
	/** Number of Triples with this Property */
	usageCount: Scalars['Union']['output']
	/** Number of Wikibases Used */
	wikibaseCount: Scalars['Union']['output']
}

export type WikibasePropertyPopularityAggregateCountPage = {
	__typename?: 'WikibasePropertyPopularityAggregateCountPage'
	/** Data */
	data: Array<WikibasePropertyPopularityAggregateCount>
	/** Metadata */
	meta: PageMetadata
}

export type WikibasePropertyPopularityCount = {
	__typename?: 'WikibasePropertyPopularityCount'
	id: Scalars['ID']['output']
	/** Property URL */
	propertyUrl: Scalars['String']['output']
	/** Number of Triples with this Property */
	usageCount: Scalars['Union']['output']
}

export type WikibasePropertyPopularityObservation = {
	__typename?: 'WikibasePropertyPopularityObservation'
	id: Scalars['ID']['output']
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Number of Items with Number of Relationships */
	propertyPopularityCounts: Array<WikibasePropertyPopularityCount>
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
}

export type WikibasePropertyPopularityObservationWikibaseObservationSet = {
	__typename?: 'WikibasePropertyPopularityObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibasePropertyPopularityObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibasePropertyPopularityObservation>
}

export type WikibaseQuantityAggregate = {
	__typename?: 'WikibaseQuantityAggregate'
	/** Total Items */
	totalItems: Scalars['Union']['output']
	/** Total Lexemes */
	totalLexemes: Scalars['Union']['output']
	/** Total Properties */
	totalProperties: Scalars['Union']['output']
	/** Total Triples */
	totalTriples: Scalars['Union']['output']
	/** Wikibases with Quantity Data */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseQuantityObservation = {
	__typename?: 'WikibaseQuantityObservation'
	id: Scalars['ID']['output']
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
	/** Total Items */
	totalItems?: Maybe<Scalars['Union']['output']>
	/** Total Lexemes */
	totalLexemes?: Maybe<Scalars['Union']['output']>
	/** Total Properties */
	totalProperties?: Maybe<Scalars['Union']['output']>
	/** Total Triples */
	totalTriples?: Maybe<Scalars['Union']['output']>
}

export type WikibaseQuantityObservationWikibaseObservationSet = {
	__typename?: 'WikibaseQuantityObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseQuantityObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseQuantityObservation>
}

export type WikibaseRecentChangesAggregate = {
	__typename?: 'WikibaseRecentChangesAggregate'
	/** Total Bot Editors with 5+ edits in the last 30 days across Wikibase instances */
	botChangeActiveUserCount: Scalars['Union']['output']
	/** Total Bot Changes in the last 30 days across Wikibase instances */
	botChangeCount: Scalars['Union']['output']
	/** Total Bot Editors in the last 30 days across Wikibase instances */
	botChangeUserCount: Scalars['Union']['output']
	/** Total Human Editors with 5+ edits in the last 30 days across Wikibase instances */
	humanChangeActiveUserCount: Scalars['Union']['output']
	/** Total Human Changes in the last 30 days across Wikibase instances */
	humanChangeCount: Scalars['Union']['output']
	/** Total Human Editors in the last 30 days across Wikibase instances */
	humanChangeUserCount: Scalars['Union']['output']
	/** Wikibases with Recent Changes Data */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseRecentChangesObservation = {
	__typename?: 'WikibaseRecentChangesObservation'
	/** Number of unique bots with at least 5 records found in changes requested with bot flag, derived from all bot/usernames. */
	botChangeActiveUserCount?: Maybe<Scalars['Union']['output']>
	/** Number of changes made by bots as reported by the MediaWiki Recent Changes API when called with the bot flag. */
	botChangeCount?: Maybe<Scalars['Union']['output']>
	/** Number of unique bots found in changes requested with bot flag, derived from all bot/usernames. */
	botChangeUserCount?: Maybe<Scalars['Union']['output']>
	/** Date of first change, no matter if it was made by a human or bot. */
	firstChangeDate?: Maybe<Scalars['DateTime']['output']>
	/** Number of unique users with at least 5 records found in changes requested with !bot flag, derived from all usernames, IP addresses for anonymous edits as well as userid in the userhidden case. */
	humanChangeActiveUserCount?: Maybe<Scalars['Union']['output']>
	/** Number of changes made by humans as reported by the MediaWiki Recent Changes API when called with the !bot flag. */
	humanChangeCount?: Maybe<Scalars['Union']['output']>
	/** Number of unique users found in changes requested with !bot flag, derived from all usernames, IP addresses for anonymous edits as well as userid in the userhidden case. */
	humanChangeUserCount?: Maybe<Scalars['Union']['output']>
	id: Scalars['ID']['output']
	/** Date of last change, no matter if it was made by a human or bot. */
	lastChangeDate?: Maybe<Scalars['DateTime']['output']>
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
}

export type WikibaseRecentChangesObservationWikibaseObservationSet = {
	__typename?: 'WikibaseRecentChangesObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseRecentChangesObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseRecentChangesObservation>
}

export type WikibaseSoftware = {
	__typename?: 'WikibaseSoftware'
	/** Archived Extension */
	archived?: Maybe<Scalars['Boolean']['output']>
	/** Description */
	description?: Maybe<Scalars['String']['output']>
	/** Date Fetched from MediaWiki */
	fetched?: Maybe<Scalars['DateTime']['output']>
	id: Scalars['ID']['output']
	/** Latest Version */
	latestVersion?: Maybe<Scalars['String']['output']>
	/** Bundled with MediaWiki */
	mediawikiBundled?: Maybe<Scalars['Boolean']['output']>
	/** Public Wikis Using */
	publicWikiCount?: Maybe<Scalars['Int']['output']>
	/** Quarterly Downloads */
	quarterlyDownloadCount?: Maybe<Scalars['Int']['output']>
	/** Wikibase Software Name */
	softwareName: Scalars['String']['output']
	/** Wikibase Software Type */
	softwareType: WikibaseSoftwareType
	/** Tag List */
	tags: Array<Scalars['String']['output']>
	/** Reference URL */
	url?: Maybe<Scalars['String']['output']>
	/** Bundled with Wikibase Suite */
	wikibaseSuiteBundled?: Maybe<Scalars['Boolean']['output']>
}

export type WikibaseSoftwareMajorVersionAggregate = {
	__typename?: 'WikibaseSoftwareMajorVersionAggregate'
	/** Minor Versions */
	minorVersions?: Maybe<Array<WikibaseSoftwareMinorVersionAggregate>>
	/** Software Version */
	version?: Maybe<Scalars['String']['output']>
	/** Wikibase Count */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseSoftwareMinorVersionAggregate = {
	__typename?: 'WikibaseSoftwareMinorVersionAggregate'
	/** Patch Versions */
	patchVersions?: Maybe<Array<WikibaseSoftwarePatchVersionAggregate>>
	/** Software Version */
	version?: Maybe<Scalars['String']['output']>
	/** Wikibase Count */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseSoftwarePage = {
	__typename?: 'WikibaseSoftwarePage'
	/** Data */
	data: Array<WikibaseSoftware>
	/** Metadata */
	meta: PageMetadata
}

export type WikibaseSoftwarePatchVersionAggregate = {
	__typename?: 'WikibaseSoftwarePatchVersionAggregate'
	/** Versions */
	subVersions?: Maybe<Array<WikibaseSoftwareVersionAggregate>>
	/** Software Version */
	version?: Maybe<Scalars['String']['output']>
	/** Wikibase Count */
	wikibaseCount: Scalars['Int']['output']
}

export enum WikibaseSoftwareType {
	Extension = 'EXTENSION',
	Library = 'LIBRARY',
	Skin = 'SKIN',
	Software = 'SOFTWARE'
}

export type WikibaseSoftwareVersion = {
	__typename?: 'WikibaseSoftwareVersion'
	id: Scalars['ID']['output']
	/** Software */
	software: WikibaseSoftware
	/**
	 * Software Name
	 * @deprecated Use software/softwareName
	 */
	softwareName: Scalars['String']['output']
	/** Software Version */
	version?: Maybe<Scalars['String']['output']>
	/** Software Version Release Date */
	versionDate?: Maybe<Scalars['DateTime']['output']>
	/** Software Version Commit Hash */
	versionHash?: Maybe<Scalars['String']['output']>
}

export type WikibaseSoftwareVersionAggregate = {
	__typename?: 'WikibaseSoftwareVersionAggregate'
	/** Software Version */
	version?: Maybe<Scalars['String']['output']>
	/** Software Version */
	versionDate?: Maybe<Scalars['DateTime']['output']>
	/** Software Version */
	versionHash?: Maybe<Scalars['String']['output']>
	/** Number of Wikibases Used */
	wikibaseCount: Scalars['Union']['output']
}

export type WikibaseSoftwareVersionDoubleAggregate = {
	__typename?: 'WikibaseSoftwareVersionDoubleAggregate'
	/** Major Versions */
	majorVersions: Array<WikibaseSoftwareMajorVersionAggregate>
	/** Software Name */
	softwareName: Scalars['String']['output']
	/** Version List */
	versions: Array<WikibaseSoftwareVersionAggregate>
	/** Wikibase Count */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseSoftwareVersionDoubleAggregatePage = {
	__typename?: 'WikibaseSoftwareVersionDoubleAggregatePage'
	/** Data */
	data: Array<WikibaseSoftwareVersionDoubleAggregate>
	/** Metadata */
	meta: PageMetadata
}

export type WikibaseSoftwareVersionObservation = {
	__typename?: 'WikibaseSoftwareVersionObservation'
	id: Scalars['ID']['output']
	/** Installed Extensions w/ Versions */
	installedExtensions: Array<WikibaseSoftwareVersion>
	/** Installed Libraries w/ Versions */
	installedLibraries: Array<WikibaseSoftwareVersion>
	/** Installed Skins w/ Versions */
	installedSkins: Array<WikibaseSoftwareVersion>
	/** Installed Software Versions */
	installedSoftware: Array<WikibaseSoftwareVersion>
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
}

export type WikibaseSoftwareVersionObservationWikibaseObservationSet = {
	__typename?: 'WikibaseSoftwareVersionObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseSoftwareVersionObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseSoftwareVersionObservation>
}

export type WikibaseStatisticsAggregate = {
	__typename?: 'WikibaseStatisticsAggregate'
	edits: WikibaseStatisticsEditsObservation
	files: WikibaseStatisticsFilesObservation
	pages: WikibaseStatisticsPagesObservation
	users: WikibaseStatisticsUsersObservation
	/** Wikibases with Statistics Data */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseStatisticsEditsObservation = {
	__typename?: 'WikibaseStatisticsEditsObservation'
	/** Average Edits per Page */
	editsPerPageAvg?: Maybe<Scalars['Float']['output']>
	/** Total Edits */
	totalEdits: Scalars['Union']['output']
}

export type WikibaseStatisticsFilesObservation = {
	__typename?: 'WikibaseStatisticsFilesObservation'
	/** Total Files */
	totalFiles?: Maybe<Scalars['Union']['output']>
}

export type WikibaseStatisticsObservation = {
	__typename?: 'WikibaseStatisticsObservation'
	edits?: Maybe<WikibaseStatisticsEditsObservation>
	files?: Maybe<WikibaseStatisticsFilesObservation>
	id: Scalars['ID']['output']
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	pages?: Maybe<WikibaseStatisticsPagesObservation>
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
	users?: Maybe<WikibaseStatisticsUsersObservation>
}

export type WikibaseStatisticsObservationWikibaseObservationSet = {
	__typename?: 'WikibaseStatisticsObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseStatisticsObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseStatisticsObservation>
}

export type WikibaseStatisticsPagesObservation = {
	__typename?: 'WikibaseStatisticsPagesObservation'
	/** Content Page Word Count - Average */
	contentPageWordCountAvg?: Maybe<Scalars['Float']['output']>
	/** Content Page Word Count - Total */
	contentPageWordCountTotal?: Maybe<Scalars['Union']['output']>
	/** Content Pages */
	contentPages: Scalars['Union']['output']
	/** Total Pages */
	totalPages: Scalars['Union']['output']
}

export type WikibaseStatisticsUsersObservation = {
	__typename?: 'WikibaseStatisticsUsersObservation'
	/** Active Users */
	activeUsers: Scalars['Union']['output']
	/** Total Admin */
	totalAdmin: Scalars['Union']['output']
	/** Total Users */
	totalUsers: Scalars['Union']['output']
}

export type WikibaseTimeToFirstValueObservation = {
	__typename?: 'WikibaseTimeToFirstValueObservation'
	id: Scalars['ID']['output']
	/** Wikibase Initiation Date */
	initiationDate?: Maybe<Scalars['DateTime']['output']>
	/** Item Creation Date */
	itemDates: Array<WikibaseItemDate>
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
}

export type WikibaseTimeToFirstValueObservationWikibaseObservationSet = {
	__typename?: 'WikibaseTimeToFirstValueObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseTimeToFirstValueObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseTimeToFirstValueObservation>
}

export enum WikibaseType {
	Cloud = 'CLOUD',
	Other = 'OTHER',
	Suite = 'SUITE',
	Test = 'TEST'
}

export type WikibaseTypeInput = {
	exclude?: InputMaybe<Array<WikibaseType>>
}

export type WikibaseUrlSet = {
	__typename?: 'WikibaseURLSet'
	/**
	 * Action API URL
	 * @deprecated Use scriptPath
	 */
	actionApi?: Maybe<Scalars['String']['output']>
	/** Article Path `/wiki` */
	articlePath?: Maybe<Scalars['String']['output']>
	/** Base URL */
	baseUrl: Scalars['String']['output']
	/**
	 * Index API URL
	 * @deprecated Use scriptPath
	 */
	indexApi?: Maybe<Scalars['String']['output']>
	/** Script Path `/w` */
	scriptPath?: Maybe<Scalars['String']['output']>
	/** SPARQL Endpoint URL */
	sparqlEndpointUrl?: Maybe<Scalars['String']['output']>
	/** SPARQL Frontend URL */
	sparqlFrontendUrl?: Maybe<Scalars['String']['output']>
	/**
	 * SPARQL URL
	 * @deprecated Renamed to sparqlFrontendURL for clarity
	 */
	sparqlUrl?: Maybe<Scalars['String']['output']>
	/**
	 * Special:Statistics URL
	 * @deprecated Use articlePath
	 */
	specialStatisticsUrl?: Maybe<Scalars['String']['output']>
	/**
	 * Special:Version URL
	 * @deprecated Use articlePath
	 */
	specialVersionUrl?: Maybe<Scalars['String']['output']>
}

export type WikibaseUrlSetInput = {
	articlePath?: InputMaybe<Scalars['String']['input']>
	baseUrl: Scalars['String']['input']
	scriptPath?: InputMaybe<Scalars['String']['input']>
	sparqlEndpointUrl?: InputMaybe<Scalars['String']['input']>
	sparqlFrontendUrl?: InputMaybe<Scalars['String']['input']>
}

export enum WikibaseUrlType {
	ActionQueryUrl = 'ACTION_QUERY_URL',
	ArticlePath = 'ARTICLE_PATH',
	BaseUrl = 'BASE_URL',
	IndexQueryUrl = 'INDEX_QUERY_URL',
	ScriptPath = 'SCRIPT_PATH',
	SparqlEndpointUrl = 'SPARQL_ENDPOINT_URL',
	SparqlFrontendUrl = 'SPARQL_FRONTEND_URL',
	SparqlQueryUrl = 'SPARQL_QUERY_URL',
	SpecialStatisticsUrl = 'SPECIAL_STATISTICS_URL',
	SpecialVersionUrl = 'SPECIAL_VERSION_URL'
}

export type WikibaseUserAggregate = {
	__typename?: 'WikibaseUserAggregate'
	/** Total Administrators (estimated from group names) */
	totalAdmin: Scalars['Union']['output']
	/** Total Users in all Wikibases (DOES NOT ACCOUNT FOR OVERLAP) */
	totalUsers: Scalars['Union']['output']
	/** Wikibases with User Data */
	wikibaseCount: Scalars['Int']['output']
}

export type WikibaseUserGroup = {
	__typename?: 'WikibaseUserGroup'
	/** Group Name */
	groupName: Scalars['String']['output']
	id: Scalars['ID']['output']
	/** Wikibase Default Group? */
	wikibaseDefault: Scalars['Boolean']['output']
}

export type WikibaseUserObservation = {
	__typename?: 'WikibaseUserObservation'
	id: Scalars['ID']['output']
	/** Observation Date */
	observationDate: Scalars['DateTime']['output']
	/** Returned Data? */
	returnedData: Scalars['Boolean']['output']
	/** Total Users */
	totalUsers?: Maybe<Scalars['Union']['output']>
	/** User Groups and Counts */
	userGroups: Array<WikibaseUserObservationGroup>
}

export type WikibaseUserObservationGroup = {
	__typename?: 'WikibaseUserObservationGroup'
	group: WikibaseUserGroup
	/** Group Marked Implicit? */
	groupImplicit: Scalars['Boolean']['output']
	id: Scalars['ID']['output']
	/** User Count */
	userCount: Scalars['Union']['output']
}

export type WikibaseUserObservationWikibaseObservationSet = {
	__typename?: 'WikibaseUserObservationWikibaseObservationSet'
	/** All Observations */
	allObservations: Array<WikibaseUserObservation>
	/** Most Recent Observation that Returned Data */
	mostRecent?: Maybe<WikibaseUserObservation>
}

export enum WikibaseUserType {
	Bot = 'BOT',
	Missing = 'MISSING',
	None = 'NONE',
	User = 'USER'
}

export type WikibaseYearCreatedAggregate = {
	__typename?: 'WikibaseYearCreatedAggregate'
	/** Wikibase Count Count */
	wikibaseCount: Scalars['Union']['output']
	/** Year of First Log */
	year: Scalars['Union']['output']
}

export type SingleWikibaseQueryVariables = Exact<{
	wikibaseId: Scalars['Int']['input']
}>

export type SingleWikibaseQuery = {
	__typename?: 'Query'
	wikibase: { __typename?: 'Wikibase' } & {
		' $fragmentRefs'?: { SingleWikibaseFragment: SingleWikibaseFragment }
	}
}

export type SingleWikibaseFragment = {
	__typename?: 'Wikibase'
	id: string
	title: string
	description?: string | null
	wikibaseType?: WikibaseType | null
	urls: { __typename?: 'WikibaseURLSet'; baseUrl: string; sparqlFrontendUrl?: string | null }
	quantityObservations: {
		__typename?: 'WikibaseQuantityObservationWikibaseObservationSet'
		mostRecent?: {
			__typename?: 'WikibaseQuantityObservation'
			observationDate: Date
			totalItems?: number | null
			totalLexemes?: number | null
			totalProperties?: number | null
			totalTriples?: number | null
		} | null
	}
	recentChangesObservations: {
		__typename?: 'WikibaseRecentChangesObservationWikibaseObservationSet'
		mostRecent?: {
			__typename?: 'WikibaseRecentChangesObservation'
			observationDate: Date
			botChangeCount?: number | null
			humanChangeCount?: number | null
		} | null
	}
	timeToFirstValueObservations: {
		__typename?: 'WikibaseTimeToFirstValueObservationWikibaseObservationSet'
		mostRecent?: {
			__typename?: 'WikibaseTimeToFirstValueObservation'
			observationDate: Date
			initiationDate?: Date | null
		} | null
	}
} & { ' $fragmentName'?: 'SingleWikibaseFragment' }

export type PageWikibasesQueryVariables = Exact<{
	pageNumber: Scalars['Int']['input']
	pageSize: Scalars['Int']['input']
	wikibaseFilter?: InputMaybe<WikibaseFilterInput>
}>

export type PageWikibasesQuery = {
	__typename?: 'Query'
	wikibaseList: {
		__typename?: 'WikibasePage'
		meta: { __typename?: 'PageMetadata'; totalCount: number }
		data: Array<{ __typename?: 'Wikibase' } & { ' $fragmentRefs'?: { WbFragment: WbFragment } }>
	}
}

export type WbFragment = {
	__typename?: 'Wikibase'
	id: string
	title: string
	description?: string | null
	wikibaseType?: WikibaseType | null
	urls: { __typename?: 'WikibaseURLSet'; baseUrl: string }
	quantityObservations: {
		__typename?: 'WikibaseQuantityObservationWikibaseObservationSet'
		mostRecent?: { __typename?: 'WikibaseQuantityObservation'; totalTriples?: number | null } | null
	}
	recentChangesObservations: {
		__typename?: 'WikibaseRecentChangesObservationWikibaseObservationSet'
		mostRecent?: {
			__typename?: 'WikibaseRecentChangesObservation'
			botChangeCount?: number | null
			humanChangeCount?: number | null
		} | null
	}
} & { ' $fragmentName'?: 'WbFragment' }

export const SingleWikibaseFragmentDoc = {
	kind: 'Document',
	definitions: [
		{
			kind: 'FragmentDefinition',
			name: { kind: 'Name', value: 'SingleWikibase' },
			typeCondition: { kind: 'NamedType', name: { kind: 'Name', value: 'Wikibase' } },
			selectionSet: {
				kind: 'SelectionSet',
				selections: [
					{ kind: 'Field', name: { kind: 'Name', value: 'id' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'title' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'description' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'urls' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{ kind: 'Field', name: { kind: 'Name', value: 'baseUrl' } },
								{ kind: 'Field', name: { kind: 'Name', value: 'sparqlFrontendUrl' } }
							]
						}
					},
					{ kind: 'Field', name: { kind: 'Name', value: 'wikibaseType' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'quantityObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'observationDate' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalItems' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalLexemes' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalProperties' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalTriples' } }
										]
									}
								}
							]
						}
					},
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'recentChangesObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'observationDate' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'botChangeCount' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'humanChangeCount' } }
										]
									}
								}
							]
						}
					},
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'timeToFirstValueObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'observationDate' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'initiationDate' } }
										]
									}
								}
							]
						}
					}
				]
			}
		}
	]
} as unknown as DocumentNode<SingleWikibaseFragment, unknown>
export const WbFragmentDoc = {
	kind: 'Document',
	definitions: [
		{
			kind: 'FragmentDefinition',
			name: { kind: 'Name', value: 'WB' },
			typeCondition: { kind: 'NamedType', name: { kind: 'Name', value: 'Wikibase' } },
			selectionSet: {
				kind: 'SelectionSet',
				selections: [
					{ kind: 'Field', name: { kind: 'Name', value: 'id' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'title' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'description' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'urls' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [{ kind: 'Field', name: { kind: 'Name', value: 'baseUrl' } }]
						}
					},
					{ kind: 'Field', name: { kind: 'Name', value: 'wikibaseType' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'quantityObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [{ kind: 'Field', name: { kind: 'Name', value: 'totalTriples' } }]
									}
								}
							]
						}
					},
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'recentChangesObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'botChangeCount' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'humanChangeCount' } }
										]
									}
								}
							]
						}
					}
				]
			}
		}
	]
} as unknown as DocumentNode<WbFragment, unknown>
export const SingleWikibaseDocument = {
	kind: 'Document',
	definitions: [
		{
			kind: 'OperationDefinition',
			operation: 'query',
			name: { kind: 'Name', value: 'SingleWikibase' },
			variableDefinitions: [
				{
					kind: 'VariableDefinition',
					variable: { kind: 'Variable', name: { kind: 'Name', value: 'wikibaseId' } },
					type: {
						kind: 'NonNullType',
						type: { kind: 'NamedType', name: { kind: 'Name', value: 'Int' } }
					}
				}
			],
			selectionSet: {
				kind: 'SelectionSet',
				selections: [
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'wikibase' },
						arguments: [
							{
								kind: 'Argument',
								name: { kind: 'Name', value: 'wikibaseId' },
								value: { kind: 'Variable', name: { kind: 'Name', value: 'wikibaseId' } }
							}
						],
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{ kind: 'FragmentSpread', name: { kind: 'Name', value: 'SingleWikibase' } }
							]
						}
					}
				]
			}
		},
		{
			kind: 'FragmentDefinition',
			name: { kind: 'Name', value: 'SingleWikibase' },
			typeCondition: { kind: 'NamedType', name: { kind: 'Name', value: 'Wikibase' } },
			selectionSet: {
				kind: 'SelectionSet',
				selections: [
					{ kind: 'Field', name: { kind: 'Name', value: 'id' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'title' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'description' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'urls' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{ kind: 'Field', name: { kind: 'Name', value: 'baseUrl' } },
								{ kind: 'Field', name: { kind: 'Name', value: 'sparqlFrontendUrl' } }
							]
						}
					},
					{ kind: 'Field', name: { kind: 'Name', value: 'wikibaseType' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'quantityObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'observationDate' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalItems' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalLexemes' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalProperties' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'totalTriples' } }
										]
									}
								}
							]
						}
					},
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'recentChangesObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'observationDate' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'botChangeCount' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'humanChangeCount' } }
										]
									}
								}
							]
						}
					},
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'timeToFirstValueObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'observationDate' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'initiationDate' } }
										]
									}
								}
							]
						}
					}
				]
			}
		}
	]
} as unknown as DocumentNode<SingleWikibaseQuery, SingleWikibaseQueryVariables>
export const PageWikibasesDocument = {
	kind: 'Document',
	definitions: [
		{
			kind: 'OperationDefinition',
			operation: 'query',
			name: { kind: 'Name', value: 'PageWikibases' },
			variableDefinitions: [
				{
					kind: 'VariableDefinition',
					variable: { kind: 'Variable', name: { kind: 'Name', value: 'pageNumber' } },
					type: {
						kind: 'NonNullType',
						type: { kind: 'NamedType', name: { kind: 'Name', value: 'Int' } }
					}
				},
				{
					kind: 'VariableDefinition',
					variable: { kind: 'Variable', name: { kind: 'Name', value: 'pageSize' } },
					type: {
						kind: 'NonNullType',
						type: { kind: 'NamedType', name: { kind: 'Name', value: 'Int' } }
					}
				},
				{
					kind: 'VariableDefinition',
					variable: { kind: 'Variable', name: { kind: 'Name', value: 'wikibaseFilter' } },
					type: { kind: 'NamedType', name: { kind: 'Name', value: 'WikibaseFilterInput' } }
				}
			],
			selectionSet: {
				kind: 'SelectionSet',
				selections: [
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'wikibaseList' },
						arguments: [
							{
								kind: 'Argument',
								name: { kind: 'Name', value: 'wikibaseFilter' },
								value: { kind: 'Variable', name: { kind: 'Name', value: 'wikibaseFilter' } }
							},
							{
								kind: 'Argument',
								name: { kind: 'Name', value: 'pageNumber' },
								value: { kind: 'Variable', name: { kind: 'Name', value: 'pageNumber' } }
							},
							{
								kind: 'Argument',
								name: { kind: 'Name', value: 'pageSize' },
								value: { kind: 'Variable', name: { kind: 'Name', value: 'pageSize' } }
							}
						],
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'meta' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [{ kind: 'Field', name: { kind: 'Name', value: 'totalCount' } }]
									}
								},
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'data' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [{ kind: 'FragmentSpread', name: { kind: 'Name', value: 'WB' } }]
									}
								}
							]
						}
					}
				]
			}
		},
		{
			kind: 'FragmentDefinition',
			name: { kind: 'Name', value: 'WB' },
			typeCondition: { kind: 'NamedType', name: { kind: 'Name', value: 'Wikibase' } },
			selectionSet: {
				kind: 'SelectionSet',
				selections: [
					{ kind: 'Field', name: { kind: 'Name', value: 'id' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'title' } },
					{ kind: 'Field', name: { kind: 'Name', value: 'description' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'urls' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [{ kind: 'Field', name: { kind: 'Name', value: 'baseUrl' } }]
						}
					},
					{ kind: 'Field', name: { kind: 'Name', value: 'wikibaseType' } },
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'quantityObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [{ kind: 'Field', name: { kind: 'Name', value: 'totalTriples' } }]
									}
								}
							]
						}
					},
					{
						kind: 'Field',
						name: { kind: 'Name', value: 'recentChangesObservations' },
						selectionSet: {
							kind: 'SelectionSet',
							selections: [
								{
									kind: 'Field',
									name: { kind: 'Name', value: 'mostRecent' },
									selectionSet: {
										kind: 'SelectionSet',
										selections: [
											{ kind: 'Field', name: { kind: 'Name', value: 'botChangeCount' } },
											{ kind: 'Field', name: { kind: 'Name', value: 'humanChangeCount' } }
										]
									}
								}
							]
						}
					}
				]
			}
		}
	]
} as unknown as DocumentNode<PageWikibasesQuery, PageWikibasesQueryVariables>
